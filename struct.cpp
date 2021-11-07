#include<iostream>
#include<vector>
#include<map>

using namespace std;

class AFN{
    public:
    AFN(){
        cin>>n_estados>>e_inicial>>n_e_finales;
        int temp;
        for(int i = 0; i < n_e_finales; i++){
            cin>>temp;
            e_finales.push_back(temp);
        }
    }
    private:
    int n_estados, e_inicial, n_e_finales;
    vector<int>e_finales;

};

int main(){
    AFN test1();
    return 0;
}