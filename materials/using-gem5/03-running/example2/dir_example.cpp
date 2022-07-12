#include<iostream>
#include<dirent.h>

using namespace std;

int main()
{
    struct dirent *d;
    DIR *dr;
    dr = opendir("/workspaces/gem5-bootcamp-env/materials/using-gem5/03-running");
    if (dr!=NULL) {
        std::cout<<"List of Files & Folders:\n";
        for (d=readdir(dr); d!=NULL; d=readdir(dr)) {
            std::cout<<d->d_name<< ", ";
        }
        closedir(dr);
    }
    else {
        std::cout<<"\nError Occurred!";
    }
    std::cout<<endl;
    return 0;
}


