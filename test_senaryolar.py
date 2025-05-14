from veriyapıları import Queue, Stack, LinkedList
from bagajj import Passenger, esya_tehlikeli_mi, YASAKLAR

def test_queue():
    q = Queue()
    p1 = Passenger()
    p2 = Passenger()
    q.enqueue(p1)
    q.enqueue(p2)
    assert q.dequeue() == p1
    assert q.dequeue() == p2
    assert q.is_empty()
    print("Queue testi başarılı.")

def test_stack():
    s = Stack()
    s.push("a")
    s.push("b")
    assert s.pop() == "b"
    assert s.pop() == "a"
    assert s.is_empty()
    print("Stack testi başarılı.")

def test_linkedlist():
    l = LinkedList()
    l.append("X")
    l.append("Y")
    assert l.contains("X")
    assert not l.contains("Z")
    print("LinkedList testi başarılı.")

def test_esya_tehlikeli_mi():
    for esya in YASAKLAR:
        assert esya_tehlikeli_mi(esya)
    assert not esya_tehlikeli_mi("kitap")
    print("Tehlikeli eşya testi başarılı.")

def test_passenger_bagaj():
    p = Passenger()
    assert 5 <= len(p.bagaj) <= 10
    print("Yolcu bagaj testi başarılı.")
