#include<iostream>
#include<vector>
#include<unordered_map>

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
        /* for(int i = 0; i<n_estados*2; i++){
            transiciones.insert({0,{2,3}});
        } */
    }
    private:
    int n_estados, e_inicial, n_e_finales;
    vector<int>e_finales;
    unordered_map<int, int[2]> transiciones;
};

int main(){
    AFN test1();
    return 0;
}