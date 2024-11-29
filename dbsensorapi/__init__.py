import sys
import click
import traceback
from smbus2 import SMBus
from flask import Flask, Response
from threading import Event, Lock, Thread
from statistics import fmean


class Sensor:
    def __init__(self, bus: SMBus, address: int, poll_rate: int, average_count: int):
        self.bus = bus
        self.poll_rate = poll_rate
        self.average_count = average_count
        self.address = address

        self.current_average = None
        self.current_max = None
        self.thread = None
        self.event = Event()
        self.lock = Lock()


    def run(self):
        print('Poll thread starting')

        try:
            values = []

            while not self.event.is_set():
                value = self.bus.read_byte_data(self.address, 0x0A)

                values.append(float(value))

                if len(values) > self.average_count:
                    del values[0]

                with self.lock:
                    self.current_max = max(values)
                    self.current_average = fmean(values)

                if self.event.wait(self.poll_rate):
                    break

        except:
            print(f'Caught exception on polling thread: {traceback.format_exc()}')

        print('Poll thread exiting')


    def __enter__(self):
        assert self.thread is None

        self.thread = Thread(target=self.run)
        self.thread.start()

        return self

    def __exit__(self, *args, **kwargs):
        self.event.set()

        if self.thread is not None:
            self.thread.join()

    def value(self) -> float:
        with self.lock:
            return self.current_average, self.current_max

@click.command()
@click.option('--listen-address', default='127.0.0.1')
@click.option('--listen-port', default=8000, type=int)
@click.option('--i2c-bus', default=1, type=int)
@click.option('--i2c-address', default=0x48, type=int)
@click.option('--poll-rate', default=1, type=int)
@click.option('--average-count', default=60, type=int)
def main(listen_address: str, listen_port: int, i2c_bus: int, i2c_address: int, poll_rate: int, average_count: int):
    app = Flask(__name__)
    bus = SMBus(i2c_bus)

    sensor = Sensor(bus, i2c_address, poll_rate, average_count)

    @app.route('/', methods=['GET'])
    def get():
        content = 'dbsensor_average_dba {:.2f}\ndbsensor_max_dba {:.2f}\n'.format(*sensor.value())
        return content, 200


    with sensor:
        app.run(host=listen_address, port=listen_port)

if __name__ == '__main__':
    main()

