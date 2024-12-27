import random
import streamlit as st

def conflicts(board, row, col):
    """
    Calculate the number of conflicts for a queen at (row, col).
    """
    count = 0
    for r in range(len(board)):
        if r != row:
            c = board[r]
            if c == col or abs(c - col) == abs(r - row):
                count += 1
    return count

def total_conflicts(board):
    """
    Calculate the total number of conflicts for the entire board.
    """
    total = 0
    for row in range(len(board)):
        total += conflicts(board, row, board[row])
    return total

def min_conflicts(n, max_steps=1000):
    """
    Solve the N-Queens problem using the Min-Conflicts algorithm.
    """
    board = [random.randint(0, n - 1) for _ in range(n)]

    for step in range(max_steps):
        if total_conflicts(board) == 0:
            return board

        conflicted_queens = [row for row in range(n) if conflicts(board, row, board[row]) > 0]

        if not conflicted_queens:
            return board

        row = random.choice(conflicted_queens)
        conflict_counts = [conflicts(board, row, col) for col in range(n)]
        min_conflict = min(conflict_counts)
        min_conflict_cols = [col for col in range(n) if conflict_counts[col] == min_conflict]
        board[row] = random.choice(min_conflict_cols)

    return []

def generate_chessboard(board):
    """
    Generate an HTML representation of a chessboard with queens.
    """
    n = len(board)
    board_html = """
    <style>
    table {border-collapse: collapse; margin: 10px 0;}
    td {width: 40px; height: 40px; text-align: center; font-size: 24px; font-weight: bold;}
    .white {background-color: #f0d9b5;}
    .black {background-color: #b58863;}
    .queen {color: red;}
    </style>
    """
    board_html += "<table>"
    for row in range(n):
        board_html += "<tr>"
        for col in range(n):
            cell_color = "white" if (row + col) % 2 == 0 else "black"
            cell_content = "&#9813;" if board[row] == col else ""  # Chess queen symbol
            board_html += f'<td class="{cell_color}">{cell_content}</td>'
        board_html += "</tr>"
    board_html += "</table>"
    return board_html

# Streamlit app
st.title("N-Queens Solver and Validator")

st.write("Provide the size of the board and optionally a solution to validate, or let the app solve the problem for you.")

# Input section
n = st.number_input("Enter the number of queens (n):", min_value=4, max_value=500, step=1, value=8)
user_input = st.text_input(
    f"Optionally, enter your solution as a list of size {n} (e.g., 0 1 2 3 for n=4). Leave blank to find a solution:"
)

if st.button("Process"):
   if user_input.strip():  # User provided a solution
     try:
        user_board = list(map(int, user_input.split()))

        if len(user_board) != n:
            st.error("The solution's length must match the board size (n).")
        else:
            st.write("### User-Provided Solution")
            chessboard_html = generate_chessboard(user_board)
            st.markdown(chessboard_html, unsafe_allow_html=True)

            total_conflict = total_conflicts(user_board)
            st.write(f"**Total Conflicts:** {total_conflict}")

            if total_conflict == 0:
                st.success("Your solution is correct! Well done!")
            else:
                st.warning("Your solution has conflicts. Providing a corrected solution...")
                corrected_solution = min_conflicts(n, max_steps=1000)
                if corrected_solution:
                    st.success("Corrected solution found!")
                    st.write("### Corrected Chessboard")
                    corrected_chessboard_html = generate_chessboard(corrected_solution)
                    st.markdown(corrected_chessboard_html, unsafe_allow_html=True)

                    st.write("### Corrected Solution Configuration")
                    st.write(corrected_solution)
                    st.download_button(
                        label="Download Corrected Solution",
                        data="\n".join(map(str, corrected_solution)),
                        file_name="corrected_n_queens_solution.txt",
                        mime="text/plain",
                    )
                else:
                    st.error("Could not find a corrected solution within the given steps.")
     except ValueError:
        st.error("Please enter a valid list of integers separated by spaces.")
   else:  # No solution provided, solve the problem
        st.write("No solution provided. Solving the N-Queens problem...")
        solution = min_conflicts(n)
        if solution:
            st.success("Solution found!")
            st.write("### Solved Chessboard")
            chessboard_html = generate_chessboard(solution)
            st.markdown(chessboard_html, unsafe_allow_html=True)

            st.write("### Solution Configuration")
            st.write(solution)
            st.download_button(
                label="Download Solution",
                data="\n".join(map(str, solution)),
                file_name="n_queens_solution.txt",
                mime="text/plain",
            )
        else:
            st.error("No solution found within the given steps.")
