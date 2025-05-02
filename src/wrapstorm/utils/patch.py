import copy
import builtins
from storm.knowledge_storm.utils import FileIOHelper
from storm.knowledge_storm.storm_wiki.engine import STORMWikiRunner
from storm.knowledge_storm.storm_wiki.modules.storm_dataclass import StormInformationTable, StormArticle

IN_MEMORY_OUTPUTS = {} 

def patch_file_io():
    def no_op_dump_json(obj, path): IN_MEMORY_OUTPUTS[path] = obj
    def no_op_write_str(s, path): IN_MEMORY_OUTPUTS[path] = s
    def no_op_dump_url_to_info(self, path):
        url_to_info = copy.deepcopy(self.url_to_info)
        for url in url_to_info:
            url_to_info[url] = url_to_info[url].to_dict()
        IN_MEMORY_OUTPUTS[path] = url_to_info
    def no_op_dump_outline_to_file(self, path):
        outline = StormArticle.get_outline_as_list(self, add_hashtags=True, include_root=False)
        IN_MEMORY_OUTPUTS[path] = "\n".join(outline)
    def no_op_dump_article_as_plain_text(self, path):
        IN_MEMORY_OUTPUTS[path] = self.to_string() if hasattr(self, 'to_string') else str(self)
    def no_op_dump_reference_to_file(self, path):
        reference = copy.deepcopy(self.reference)
        for url in reference["url_to_info"]:
            reference["url_to_info"][url] = reference["url_to_info"][url].to_dict()
        IN_MEMORY_OUTPUTS[path] = reference

    FileIOHelper.dump_json = staticmethod(no_op_dump_json)
    FileIOHelper.write_str = staticmethod(no_op_write_str)
    StormInformationTable.dump_url_to_info = no_op_dump_url_to_info
    StormArticle.dump_outline_to_file = no_op_dump_outline_to_file
    StormArticle.dump_article_as_plain_text = no_op_dump_article_as_plain_text
    StormArticle.dump_reference_to_file = no_op_dump_reference_to_file

    _builtin_open = open
    def open_patch(file, mode='r', *args, **kwargs):
        if "w" in mode and file.endswith(".jsonl"):
            class DummyFile:
                def write(self, data): IN_MEMORY_OUTPUTS[file] = IN_MEMORY_OUTPUTS.get(file, "") + data
                def __enter__(self): return self
                def __exit__(self, *args): pass
            return DummyFile()
        return _builtin_open(file, mode, *args, **kwargs)
    builtins.open = open_patch

class MemoryStormRunner(STORMWikiRunner):
    def __init__(self, args, lm_configs, rm):
        super().__init__(args=args, lm_configs=lm_configs, rm=rm)
        self.memory_store = {}

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)
        self.memory_store['in_memory_outputs'] = dict(IN_MEMORY_OUTPUTS)
        return self.memory_store
