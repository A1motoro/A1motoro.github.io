#include <iostream>
#include <chrono>
using namespace std;

int main() {
    auto start = chrono::high_resolution_clock::now();
    
    // Force immediate output
    cout << "Hello, World!" << endl;
    cout.flush();  // Force buffer flush
    
    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::microseconds>(end - start);
    
    cout << "Program execution time: " << duration.count() << " microseconds" << endl;
    cout.flush();
    
    return 0;
}
