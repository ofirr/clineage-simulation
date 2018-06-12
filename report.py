from jinja2 import Template


def read_json_config(path):

    with open(path, 'rt') as file_in:
        return json.loads(file_in.read())


def read_textfile(directory, filename):

    with open(os.path.join(directory, filename), 'rt') as file_in:
        return file_in.read()


def convert_row_cols_to_html(rows):

    templ = """
<table border="1" style="border-spacing:0px">
{% for row in rows %}
<tr>
    {% for col in row %}
    <td align="middle">
        {{col}}
    </td>
    {% endfor %}
</tr>
{% endfor %}
</table>
"""

    template = Template(templ)
    html = template.render(rows=rows)

    return html


def convert_tsv_to_rows_cols(directory, filename):

    rows = []

    with open(os.path.join(directory, filename), 'rt') as file_in:
        lines = file_in.read().splitlines()
        for line in lines:
            cols = line.split("\t")
            rows.append(cols)

    return rows


def convert_mutation_table_to_html(directory, filename):

    rows = convert_tsv_to_rows_cols(directory, filename)

    # remove Run1_ from cell names to reduce the width of the final table
    row0 = []
    for col in rows[0]:
        row0.append(col.replace('Run1_', ''))
    rows[0] = row0

    return convert_row_cols_to_html(rows)


def convert_metrics_to_html(directory, filename):

    def to_table(df):
        rows = []
        for index, row in df.iterrows():
            rows.append([ index, row['metrics'] ])

        return convert_row_cols_to_html(rows)

    # read the first two lines that contain various metrics
    df_metrics = pd.read_csv(os.path.join(
        directory, filename), sep='\t', nrows=1)

    # transpose and rename the column to 'metrics'
    df_metrics = df_metrics.T.rename(columns={0: 'metrics'})

    # remove the first three unnecessary
    df_metrics = df_metrics.drop(['No', 'RefTree', 'Tree'], axis=0)

    half = int( len(df_metrics) / 2 )

    df1 = df_metrics.iloc[:half, :]
    df2 = df_metrics.iloc[half:, :]

    table1 = to_table(df1)
    table2 = to_table(df2)

    return '<table><tr valign="top"><td>{}</td><td>{}</td></tr></table>'.format(table1, table2)



templ = """
<html>
<head>
    <link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Open+Sans" />
    <style>
        table {
            font-family: "Open Sans";
            font-size: 14px;
        }
        .tree-img {
            width: 650px;
        }
    </style>
</head>
<body>

    {% for item in items %}
    <h1>{{item.config.contents.title}} ({{item.config.filename}})</h1>
    <hr/>

    <h2>Parameters</h2>
    <table>
    <tr>
        <td style="width:200px">Mutation:</td>
        <td>{{item.config.contents.addMutations}}</td>
    </tr>
    <tr>
        <td>Allelic Dropouts:</td>
        <td>{{item.config.contents.addAllelicDropOuts}}</td>
    </tr>
    <tr>
        <td>Noises:</td>
        <td>{{item.config.contents.addNoises}}</td>
    </tr>
    <tr>
        <td>Early Stop Population:</td>
        <td>{{item.config.contents.earlyStopPopulation}}</td>
    </tr>
    </table>

    <h2>Mutation Table</h2>
    {{item.simulation.mutationTable}}

    <p style="page-break-after: always;">&nbsp;</p>
    <p style="page-break-before: always;">&nbsp;</p>

    <table>
    <tr>
        <td>
            <img src="{{item.simulation.img}}" class="tree-img"/>
        </td>
        <td>
            <img src="{{item.reconstructed.img}}" class="tree-img"/>
        </td>
    </tr>
    </table>

    {{item.metrics}}

    <p style="page-break-after: always;">&nbsp;</p>
    <p style="page-break-before: always;">&nbsp;</p>

    {% endfor %}

</body>
</html>
"""

import json
import os
import pandas as pd



path_project = './analysis/tmc/'

with open(os.path.join(path_project, 'config.list'), 'rt') as fin:
    config_jsons = fin.read().splitlines()

items = []

for config_json in config_jsons:

    if not config_json:
        continue
    if not os.path.exists(os.path.join(path_project, config_json)):
        raise Exception("Unable to find {}".format(config_json))

    # read simulation configuration
    config = read_json_config(os.path.join(path_project, config_json))

    path_output = os.path.join(path_project, config['pathRelativeOutput'])



    item = {
        "config": {
            "filename": config_json,
            "contents": config
        },
        "simulation": {
            "mutationTable": convert_mutation_table_to_html(path_output, 'mutation_table.txt'),
            "img": config['pathRelativeOutput'] + '/simulation.newick.png'
        },
        "reconstructed": {
            "img": config['pathRelativeOutput'] + '/reconstructed.newick.png'
        },
        "metrics": convert_metrics_to_html(path_output, 'scores.raw.out')
    }

    items.append(item)


template = Template(templ)
html = template.render(items=items)

with open(os.path.join(path_project, 'report.html'), 'wt') as fout:
    fout.write(html)
    fout.write('\n')
