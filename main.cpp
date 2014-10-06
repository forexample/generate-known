#include <iostream>

const char* A();
const char* B();
const char* C();

int main() {
  std::cout << "A say: " << A() << std::endl;
  std::cout << "B say: " << B() << std::endl;
  std::cout << "C say: " << C() << std::endl;
}
