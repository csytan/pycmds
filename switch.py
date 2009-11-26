import os

# switches app.yaml and index.yaml

dir = os.path.dirname(__file__)
os.rename(os.path.join(dir, 'app.yaml'), 'app3.yaml')
os.rename(os.path.join(dir, 'app2.yaml'), 'app.yaml')
os.rename(os.path.join(dir, 'app3.yaml'), 'app2.yaml')

os.rename(os.path.join(dir, 'index.yaml'), 'index3.yaml')
os.rename(os.path.join(dir, 'index2.yaml'), 'index.yaml')
os.rename(os.path.join(dir, 'index3.yaml'), 'index2.yaml')