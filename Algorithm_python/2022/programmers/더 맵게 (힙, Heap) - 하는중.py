import heapq

def heap_sort(scoville):
    heap = []
    for n in scoville:
        heapq.heappush(heap, n)
    return heap

def solution(scoville, K):
    answer = 0
    scoville = heap_sort(scoville)
    while scoville[0] < K :
        if len(scoville) > 1 :
            first, second = heapq.heappop(scoville), heapq.heappop(scoville)
            if first + second * 2 != 0 :
                heapq.heappush(scoville, first + second * 2)
            scoville = heap_sort(scoville)
            answer += 1
        elif len(scoville) == 1 and scoville[0] < K : return -1
    return answer


# TEST CASE Ⅰ
scoville, K = [0,0,2], 2 
print(solution(scoville, K))
