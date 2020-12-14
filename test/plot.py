import logging
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def read(probe_file):

    with probe_file.open("r") as fin:
        header = fin.readline()
        logging.info(header)
        N = int(header.split("=")[1].strip())
        print(f"Reading {N} probes...")

    xyz_df = pd.read_csv(
        probe_file,
        sep=" ",
        decimal=".",
        skiprows=1,
        nrows=N,
        index_col="PROBEI",
        header=0,
    )
    # print(xyz_df)
    data_df = pd.read_csv(
        probe_file,
        sep=" ",
        decimal=".",
        skiprows=3 + N,
        nrows=None,
        header=0,
        index_col=None,
        na_values=["NaN"],
    )
    return xyz_df, data_df


import click


@click.command()
@click.option("--case", "-c", type=int, default=1, show_default=True)
@click.option("--refresh", "-r", type=int, default=2, show_default=True)
def run(case, refresh):
    cwd = Path(".").resolve().absolute()
    ax1 = plt.subplot(221)
    ax2 = plt.subplot(222, sharex=ax1)
    ax3 = plt.subplot(223, sharex=ax1)
    ax4 = plt.subplot(224, sharex=ax1)

    # make these tick labels invisible
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.setp(ax3.get_xticklabels(), visible=True)
    plt.setp(ax4.get_xticklabels(), visible=True)
    ax2.yaxis.tick_right()
    ax4.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    ax4.yaxis.set_label_position("right")
    # ax1.legend()
    plt.subplots_adjust(
        left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.1, hspace=0.1
    )
    fig = plt.gcf()
    fig.canvas.set_window_title(f"Test case: {case}")

    ax1.set(
        title="Horizontal wind speed [m/s]",
    )
    ax2.set(title="Wind direction [°]")
    ax3.set(title="Turbulence intensity [%]")
    ax4.set(title="Flow inclination [°]")
    ax1.set_xlim(auto=True)
    ax1.set_ylim(auto=True)
    ax2.set_ylim(auto=True)
    ax3.set_ylim(auto=True)
    ax4.set_ylim(auto=True)

    probe_file = cwd / f"{case:05d}.probes.dat"

    size_old = None
    while True:
        xyz_df = data_df = None
        if not probe_file.is_file():
            click.echo(f"Waiting for {probe_file.name}")
        else:
            try:
                xyz_df, data_df = read(probe_file)
            except:
                xyz_df = data_df = None

        do_update = data_df is not None

        t_max = np.nan
        if do_update:
            size_new = data_df.index.size
            data_df = data_df.astype({"Time": "float"})
            t_max = data_df.Time.max()
        else:
            plt.clf()

        if do_update and (size_new != size_old) and not np.isnan(t_max):
            #
            for probei in xyz_df.index:
                pdf = (
                    data_df.query("PROBEI == @probei")
                    .astype("float")
                    .sort_values("Time")
                )
                label = f"{probei}"
                kws = dict(label=label, lw=1)
                ax1.plot(pdf.Time, pdf.U2D, **kws)
                ax2.plot(pdf.Time, pdf.DIR, **kws)
                ax3.plot(pdf.Time, pdf.TI, **kws)
                ax4.plot(pdf.Time, pdf.INCL, **kws)

            size_old = size_new
        else:
            pass
            # plt.clf()

        plt.pause(refresh)

    # plt.show()


if __name__ == "__main__":
    run()
