from MazeGenerate import *

if __name__=="__main__":
    #定义迷宫的高
    num_rows = int(input("请输入行数: "))
    num_cols = int(input("请输入列数: "))

    # 设置起始点为左上角的点（当然也可以设置为右下角、右上角、左下角甚至是别的位置）
    start_row = 0
    start_col = 0

    # 设置终点为右下角的点
    end_row = num_rows - 1
    end_col = num_cols - 1

    Maze=Maze(num_rows,num_cols,start_row,start_col,end_row,end_col)
    Maze.Prim_MazeGenerate()
    Maze.Show_Maze()