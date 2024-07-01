from nada_dsl import *

nada_main = lambda: [Output(sum(SecretInteger(Input(f"int{i}", p := Party("P1"))) for i in "12"), "result", p)]

if __name__ == "__main__":
    nada_main()
