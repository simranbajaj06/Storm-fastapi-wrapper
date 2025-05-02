import os
import json
import time
import threading
import logging
from dotenv import load_dotenv
from storm.knowledge_storm.storm_wiki.engine import STORMWikiRunnerArguments, STORMWikiLMConfigs
from storm.knowledge_storm.rm import SerperRM
from src.wrapstorm.api.models import StormRequest
from src.wrapstorm.utils.patch import patch_file_io, MemoryStormRunner

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

lm_configs = STORMWikiLMConfigs()
lm_configs.init_groq_model(groq_api_key=os.getenv("GROQ_API_KEY"))

serper_retriever = SerperRM(
    serper_search_api_key=os.getenv("SERPER_API_KEY"),
    k=3
)

memory_runner = MemoryStormRunner(
    args=STORMWikiRunnerArguments(output_dir="unused", search_top_k=3, max_thread_num=1),
    lm_configs=lm_configs,
    rm=serper_retriever
)

patch_file_io()

def run_storm_query_stream(payload: StormRequest):
    seen_keys = set()

    def runner():
        memory_runner.run(
            topic=payload.topic,
            do_research=payload.do_research,
            do_generate_outline=payload.do_generate_outline,
            do_generate_article=payload.do_generate_article,
            do_polish_article=payload.do_polish_article,
        )

    thread = threading.Thread(target=runner)
    thread.start()

    while thread.is_alive() or True:
        new_items = []
        for key, value in memory_runner.memory_store.get('in_memory_outputs', {}).items():
            if key not in seen_keys:
                seen_keys.add(key)
                new_items.append((key, value))

        if new_items:
            for key, value in new_items:
                yield json.dumps({key: value}) + "\n"
        if not thread.is_alive():
            for key, value in memory_runner.memory_store.get('in_memory_outputs', {}).items():
                if key not in seen_keys:
                    seen_keys.add(key)
                    yield json.dumps({key: value}) + "\n"
            break

        time.sleep(0.5)

# payload = StormRequest(
#     topic="Artificial Intelligence",
#     do_research=True,
#     do_generate_outline=True,
#     do_generate_article=True,
#     do_polish_article=True
# )

# for chunk in run_storm_query_stream(payload):
#     logger.info(chunk) 