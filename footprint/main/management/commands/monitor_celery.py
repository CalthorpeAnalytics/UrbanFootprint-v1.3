from django.core.management import BaseCommand
from celery import current_app

__author__ = 'calthorpe_associates'

class Command(BaseCommand):
    def handle(self, *args, **options):
        state = current_app.events.State()
        print 'Current Tasks: %s' % current_app.tasks.keys()

        def announce_succeeded_tasks(event):
            state.event(event)
            task_id = event['uuid']

            print('TASK SUCCEEDED: %s[%s] %s' % (
                event['name'], task_id, state[task_id].info(), ))

        def announce_failed_tasks(event):
            state.event(event)
            task_id = event['uuid']

            print('TASK FAILED: %s[%s] %s' % (
                event['name'], task_id, state[task_id].info(), ))

        def announce_dead_workers(event):
            state.event(event)
            hostname = event.get('hostname', None)

            print('Event type %s received' % event.get('type', 'undefined'))
            if hostname and not state.workers[hostname].alive:
                print('Worker %s missed heartbeats' % (hostname, ))



        with current_app.connection() as connection:
            recv = current_app.events.Receiver(connection, handlers={
                    'task-failed': announce_failed_tasks,
                    'task-succeeded': announce_succeeded_tasks,
                    'worker-heartbeat': announce_dead_workers,
            })
            recv.capture(limit=None, timeout=None, wakeup=True)
