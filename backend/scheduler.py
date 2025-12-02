"""
backend.scheduler

Simple priority scheduler for demo and educational purposes.
"""
import heapq
from datetime import datetime

class PriorityScheduler:
    """A minimal priority scheduler using a min-heap.

    Methods:
    - submit(name, priority, ticks)
    - run_tick()
    - run_ticks(n)
    - list_tasks()
    - history()
    """
    def __init__(self):
        self._heap = []
        self._seq = 0
        self._history = []

    def submit(self, name, priority=5, ticks=1):
        self._seq += 1
        task = {
            'id': self._seq,
            'name': name,
            'priority': int(priority),
            'ticks': int(ticks),
            'created_at': datetime.utcnow().isoformat() + 'Z'
        }
        heapq.heappush(self._heap, (task['priority'], self._seq, task))
        return task

    def run_tick(self):
        executed = []
        if not self._heap:
            return executed
        priority, seq, task = heapq.heappop(self._heap)
        task['ticks'] -= 1
        executed.append(task)
        self._history.append({**task, 'executed_at': datetime.utcnow().isoformat() + 'Z'})
        if task['ticks'] > 0:
            heapq.heappush(self._heap, (task['priority'], seq, task))
        return executed

    def run_ticks(self, n):
        executed = []
        for _ in range(int(n)):
            executed.extend(self.run_tick())
        return executed

    def list_tasks(self):
        return [item[2] for item in self._heap]

    def history(self):
        return list(self._history)

if __name__ == '__main__':
    s = PriorityScheduler()
    s.submit('A', 3, 2)
    s.submit('B', 1, 1)
    print('Queue:', s.list_tasks())
    print('Run 1 tick:', s.run_tick())
    print('Run 2 ticks:', s.run_ticks(2))
    print('History:', s.history())
