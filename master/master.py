from asyncio import (
    create_subprocess_shell,
    run,
    gather,
    ProactorEventLoop,
    set_event_loop,
)
from asyncio.subprocess import Process
from os.path import join, split, isfile
from os import PathLike
from sys import platform, exit
from argparse import ArgumentParser


def get_params():
    parser = ArgumentParser()
    parser.add_argument("--slavePath", default=None, help="Pass in path to slave app")
    return parser.parse_args()


def return_slave_app_path() -> PathLike:
    # Getting path to slave.py (should resolve to same from testfiles and master.py)
    return join(*split(split(split(__file__)[0])[0]), "slave", "slave.py")


async def run_app(slave_path: str) -> Process:
    """Running slave app"""
    slave_path = slave_path if slave_path else return_slave_app_path()
    return await create_subprocess_shell(f"python {slave_path}")


async def run_controller(slave_path: str) -> None:
    return_code = None

    while return_code != 0:

        proc = await run_app(slave_path)

        pid = proc.pid
        await proc.wait()
        return_code = proc.returncode

        if return_code == 0:
            print(
                f"PID: {pid}; Slave App succesfully ran and exited; Return Code: {return_code}"
            )
        else:
            print(
                f"PID: {pid}; Return Code != 0; Restarting Slave App; Return Code: {return_code}"
            )


async def main(slave_path: str) -> None:
    tasks = [run_controller(slave_path) for idx in range(5)]
    await gather(*tasks)


if __name__ == "__main__":

    slave_path = get_params().slavePath

    try:
        if slave_path and not isfile(slave_path):

            raise FileNotFoundError(
                "ERROR: '--slavePath' parameter is not a file."
                f" Bad path: {slave_path}"
            )

    except FileNotFoundError as error:

        print(error)
        exit(2)

    # Need to change eventloop for windows to run asyncio subprocesses
    if platform == "win32":
        loop = ProactorEventLoop()
        set_event_loop(loop)
        loop.run_until_complete(main(slave_path))
        loop.close()
    else:
        run(main(slave_path))
