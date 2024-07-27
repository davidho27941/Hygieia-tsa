"""
已知問題：

1. 輸出影像時，若內容含有中文，將會出現空格亂碼。    
"""
import os
import yaml
import click

import pandas as pd

from rich.console import Console

from .visualize import plot_interval, plot_time_series

console = Console()

@click.group()
def main():
    ...

@main.command(help='Command to perform the interval of selected hospital data.')
@click.option(
    "--config",
    "config_dir",
    type=click.File(mode='r'),
    required=True,
    help='Directory to the configuration yaml file.',
)
@click.option(
    "--output",
    "output_dir",
    type=click.Path(exists=True, file_okay=False, writable=True),
    required=True,
    help="Directory to output generated files.",
)
@click.option(
    "--image-type",
    "image_type",
    type=click.Choice(['png', 'jpg']),
    default='jpg',
    help='Option to configure the output type of image.',
)
@click.option(
    "--output-file-name",
    "output_file_name",
    type=str,
    default='time_interval',
    help='Specify the file name of output file (w/o file type.).',
)
@click.option(
    "--output-html",
    "output_html",
    type=bool,
    default=True,
    help='Option to export html file or not'
)
@click.option(
    "--output-image",
    "output_image",
    type=bool,
    default=False,
    help='Option to export image file or not'
)
def show_basic_info(config_dir, output_dir, image_type='png', output_file_name='time_interval', output_html=True, output_image=False):
    
    console.log('Reading configurations.')
    config = yaml.safe_load(config_dir.read())
    console.log('Done.')
    
    console.log('Leoading datasets.')
    
    data_dict = {}
    
    for item in config['datasets'].values():
        if isinstance(item, dict):
            data_dict[item['name']] = pd.read_csv(item['dir'], index_col=False)
        elif isinstance(item, list):
            for dataset in item:
                data_dict[dataset['name']] = pd.read_csv(dataset['dir'], index_col=False)
    
    console.log('Done.')
    
    console.log('Fetching start/end date from each dataset.')
    
    start_end_date = {
        name: {
            "start": data.saveTime.min(),
            "end": data.saveTime.max(),
        }
        for name, data in data_dict.items()
    }    

    console.log('Done.')

    console.log('Generating Gantt table and Gantt chart.')

    gantt_table = pd.DataFrame(start_end_date).transpose().reset_index()
    gantt_fig = plot_interval(gantt_table)
    
    console.log('Done.')
    
    console.log('Exporting files.')
    
    if output_image:
        gantt_fig.write_image(f"{output_dir}/{output_file_name}.{image_type}", format=image_type)
    
    if output_html:
        gantt_fig.write_html(f"{output_dir}/{output_file_name}.html")
    
    console.log('Done.')
    
    console.log('Visualizing time series of each dataset.')
    
    target_cols = ['WaitingVisit', 'WaitingBed', 'WaitingBeingInHospital', 'WaitingICUBed']
    
    ts_figures = {
        name: plot_time_series(data, x='saveTime', cols=target_cols, title=name)
        for name, data in data_dict.items()
    }    
    
    console.log('Done.')
    
    console.log('Exporting files.')
    
    for name, figure in ts_figures.items():
        if output_image:
            figure.write_image(f"{output_dir}/{name}_time_series.{image_type}", format=image_type)
            
        if output_html:
            figure.write_html(f"{output_dir}/{name}_time_series.html")
    
    console.log('Done.')
    

@main.command(help='Command to apply data aggregation.')
@click.option(
    "--config",
    "config_dir",
    type=click.File(mode='r'),
    required=True,
    help='Directory to the configuration yaml file.',
)
@click.option(
    "--output",
    "output",
    type=click.Path(exists=True, file_okay=False, writable=True),
    required=True,
    help="Directory to output generated files.",
)
def aggregate_area_data(config_dir, output):
    ...

@main.command(help='Command to apply time series analysis and visualization.')
@click.option(
    "--config",
    "config_dir",
    type=click.File(mode='r'),
    required=True,
    help='Directory to the configuration yaml file.',
)
@click.option(
    "--output",
    "output",
    type=click.Path(exists=True, file_okay=False, writable=True),
    required=True,
    help="Directory to output generated files.",
)
def apply_tsa(config_dir, output):
    ...
    
    
if __name__ == '__main__':
    main()