from setuptools import setup

setup()
# docker build --tag raindata5/gourmand-api .
# docker images --quiet --filter=dangling=true | xargs --no-run-if-empty docker rmi
# docker push raindata5/gourmand-api