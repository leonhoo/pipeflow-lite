import logging

from example.one_context import OneContext

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == '__main__':
    pipeline = OneContext()
    result = pipeline.execute(initial_params={"key1": "value1"})
    print("Final Result: " + str(result))
