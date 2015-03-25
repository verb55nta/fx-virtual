#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<vector>
#include<numeric>

#include<stdlib.h>

#include<fftw3.h>

using namespace std;

int main(int argc,char* argv[])
{
  ifstream ifs(argv[1]);
  string str;
  vector<double> doll_bid;
  vector<double> doll_ask;
  

  
  while(ifs >> str){
    //cout << str << endl;
    istringstream istr(str);
    string temp;
    vector<string> result;
    while(getline(istr,temp,':')) result.push_back(temp);
    //cout << result[2] << "," << result[4] << endl;
    doll_bid.push_back(atof(result[2].c_str()));
    doll_ask.push_back(atof(result[4].c_str()));
    
    //cout << "doll-bid->" << doll_bid.back() << endl;
    //cout << "doll-ask->" << doll_ask.back() << endl;
  }
  double ave = accumulate(doll_bid.begin(),doll_bid.end(),0.0) / doll_bid.size();
  cout << "average:" << ave << endl;

  for(int i=0;i<doll_bid.size();i++){
    doll_bid[i] -= ave;
    //cout << "bid" << doll_bid[i] << endl;
  }

  ifs.close();
  
  fftw_complex *in_bid = NULL;
  fftw_complex *in_ask = NULL;
  fftw_complex *out_bid = NULL;
  fftw_complex *out_ask = NULL;
  fftw_plan p_bid,p_ask;
  
  size_t mem_size_bid = sizeof(fftw_complex) * doll_bid.size();
  size_t mem_size_ask = sizeof(fftw_complex) * doll_ask.size();
  
  in_bid = (fftw_complex*)fftw_malloc(mem_size_bid);
  out_bid = (fftw_complex*)fftw_malloc(mem_size_bid);
  in_ask = (fftw_complex*)fftw_malloc(mem_size_ask);
  out_ask = (fftw_complex*)fftw_malloc(mem_size_ask);
  
  p_bid = fftw_plan_dft_1d(doll_bid.size(),in_bid,out_bid,FFTW_FORWARD,FFTW_ESTIMATE);
  
  for(int i=0;i<doll_bid.size();i++){
    in_bid[i][0] = doll_bid[i];
    in_bid[i][1] = 0;
  }
  
  fftw_execute(p_bid);
  
  for(int i=0;i<doll_bid.size();i++){
    out_bid[i][0] /= doll_bid.size();
    out_bid[i][1] /= doll_bid.size();
  }
  
  //cout << "begin" << endl;
  
  for(int i=0;i<doll_bid.size();i++){
    cout << out_bid[i][0] << "," << out_bid[i][1] << endl;
  }
    
  return 0;
}
