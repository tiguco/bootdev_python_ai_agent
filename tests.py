from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def filet01():
    ret = get_file_content("calculator", "lorem.txt")
    print(ret)

def filet02():
    ret = get_file_content("calculator", "main.py")
    print(ret)

def filet03():
    ret = get_file_content("calculator", "pkg/calculator.py")
    print(ret)

def filet04():
    ret = get_file_content("calculator", "/bin/cat")
    print(ret)

def filet05():
    ret = get_file_content("calculator", "pkg/does_not_exist.py")
    print(ret)


def file_tests():
    filet02()
    filet03()
    filet04()
    filet05()

def write_tst01():
    ret = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(ret)

def write_tst02():
    ret = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(ret)

def write_tst03():
    ret = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(ret)


def write_tests():
    write_tst01()
    write_tst02()
    write_tst03()

def myrun():
    #ret = run_python_file("calculator", "simple.py", ["-v"])
    #ret = run_python_file("calculator", "simple.py", [] )
    ret = run_python_file("/tmp", "simple.py", [] )
    print(ret)

def run_file_t01():
    ret = run_python_file("calculator", "main.py") 
    print(ret)

def run_file_t02():
    ret = run_python_file("calculator", "main.py", ["3 + 5"]) 
    print(ret)

def run_file_t03():
    ret = run_python_file("calculator", "tests.py")
    print(ret)

def run_file_t04():
    ret = run_python_file("calculator", "../main.py") 
    print(ret)

def run_file_t05():
    ret = run_python_file("calculator", "nonexistent.py")
    print(ret)

def run_python_tests():
    run_file_t01()
    run_file_t02()
    run_file_t03()
    run_file_t04()
    run_file_t05()
    #myrun()


#write_tests()
run_python_tests()




