for c in range(int(input())):
    sudoku = [list(map(int, input().split())) for i in range(9)] # 스도쿠 만들기
    row, col, box = 0,0,0
    li = []
    for i in range(9):
        li = []
        if len(set(sudoku[i])) == 9 : row += 1
        for j in range(9):
            li.append(sudoku[j][i])
        if len(set(li)) == 9 : col += 1
    # 하는중
    #for i in range(3,10,3):
    #    for j in range(3):
    #        sudoku[j][i]
