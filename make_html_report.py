from jinja2 import Template
import os
import json
import pandas as pd
import argparse

from src import const
from src import utils


def read_textfile(directory, filename):

    with open(os.path.join(directory, filename), 'rt') as file_in:
        return file_in.read()


def convert_row_cols_to_html(rows, style_class_name=""):

    templ = """
<table border="1" style="border-spacing:0px" class="{{style_class_name}}">
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
    html = template.render(rows=rows, style_class_name=style_class_name)

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
            rows.append([index, row['metrics']])

        return convert_row_cols_to_html(rows, "metrics-table")

    # read the first two lines that contain various metrics
    df_metrics = pd.read_csv(os.path.join(
        directory, filename), sep='\t', nrows=1)

    # transpose and rename the column to 'metrics'
    df_metrics = df_metrics.T.rename(columns={0: 'metrics'})

    # remove the first three unnecessary
    df_metrics = df_metrics.drop(['No', 'RefTree', 'Tree'], axis=0)

    half = int(len(df_metrics) / 2)

    df1 = df_metrics.iloc[:half, :]
    df2 = df_metrics.iloc[half:, :]

    table1 = to_table(df1)
    table2 = to_table(df2)

    return ''''
<table>
<tbody>
    <tr valign="top">
        <td>{}</td>
        <td>{}</td>
    </tr>
</tbody>
</table>
'''.format(table1, table2)


def get_diff_metrics(path):

    with open(path, 'rt') as file_in:
        return json.loads(file_in.read())


def make_html(path_project, config_jsons, exclude_mutation_table):

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
        .metrics-table {
            min-width: 390px;
        }
        .similarity-score {
            font-family: "Open Sans";
            font-size: 120px;
            text-align: center;
            width: 40%;
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

    <table cellpadding="0" cellspacing="0" border="0" style="width:100%" width="100%">
    <tr>
        <td>{{item.metrics.compare1}}</td>
        <td class="similarity-score">{{item.metrics.compare2}}</td>
    </tr>
    </table>

    <p style="page-break-after: always;">&nbsp;</p>
    <p style="page-break-before: always;">&nbsp;</p>

    {% endfor %}

</body>
</html>
"""

    items = []

    for config_json in config_jsons:

        if not config_json:
            continue
        if not os.path.exists(os.path.join(path_project, config_json)):
            raise Exception("Unable to find {}".format(config_json))

        # read simulation configuration
        config = utils.read_json_config(os.path.join(path_project, config_json))

        path_output = os.path.join(
            path_project, config[const.CONFIG_PATH_RELATIVE_OUTPUT])

        path_diff_metrics = os.path.join(path_output, const.FILE_DIFF_METRICS)

        diff_metrics = get_diff_metrics(path_diff_metrics)
        similarity_score = '{0:2.1f}%'.format((diff_metrics['total'] - (
            diff_metrics['diff'] + diff_metrics['missing'])) / diff_metrics['total'] * 100.0)

        if exclude_mutation_table:
            mutation_table = "excluded"
        else:
            mutation_table = convert_mutation_table_to_html(path_output, const.FILE_MUTATION_TABLE)

        item = {
            "config": {
                "filename": config_json,
                "contents": config
            },
            "simulation": {
                "mutationTable": mutation_table,
                "img": "{}/{}.png".format(config[const.CONFIG_PATH_RELATIVE_OUTPUT], const.FILE_SIMULATION_NEWICK)
            },
            "reconstructed": {
                "img": "{}/{}.png".format(config[const.CONFIG_PATH_RELATIVE_OUTPUT], const.FILE_RECONSTRUCTED_NEWICK)
            },
            "metrics": {
                "compare1": convert_metrics_to_html(path_output, const.FILE_COMPARISON_METRICS_RAW),
                "compare2": similarity_score
            }
        }

        items.append(item)

    template = Template(templ)
    html = template.render(items=items)

    with open(os.path.join(path_project, const.FILE_REPORT_HTML), 'wt') as fout:
        fout.write(html)
        fout.write('\n')


def parse_arguments():

    parser = argparse.ArgumentParser(description='make html report')

    parser.add_argument(
        "--project",
        action="store",
        dest="path_project",
        required=True
    )

    parser.add_argument(
        "--config",
        nargs='+',
        dest="configs",
        required=True
    )

    parser.add_argument(
        "--exclude-mutation-table",
        action="store_true",
        dest="exclude_mutation_table",
        required=False
    )

    # parse arguments
    params = parser.parse_args()

    # get config json files
    config_jsons = utils.handle_config_args(
        params.path_project, params.configs
    )

    return params, config_jsons


if __name__ == "__main__":

    params, config_jsons = parse_arguments()

    make_html(params.path_project, config_jsons, params.exclude_mutation_table)
