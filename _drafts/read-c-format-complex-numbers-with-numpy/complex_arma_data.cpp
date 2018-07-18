#include <armadillo>

int main(int argc, char* argv[])
{
  arma::cx_mat rand_cx_mat = arma::randu<arma::cx_mat>(10,10);
  rand_cx_mat.save("rand_test.txt", arma::raw_ascii);
  return 0;
}
