&set_initial
    SET A #1
    SET B #1
    SET C #1

&fib_loop
    COPY A ACC
    ADD B
    JUMP_IF_ACC_GT #1597 &set_initial
    COPY ACC C // To display
    COPY B A
    COPY ACC B
    JUMP &fib_loop