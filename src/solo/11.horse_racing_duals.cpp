#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

int main()
{
	int n;
	int puissance;
	cin >> n;
	vector<int> vecPuissances;
	vector<int> vecDiffPuissance;

	for (int i = 0; i < n; i++)
	{	
		cin >> puissance;
		vecPuissances.push_back(puissance);
	}
	sort(vecPuissances.begin(), vecPuissances.end());

	for(int i = 0; i < n - 1; i++)
	{
		vecDiffPuissance.push_back(abs(vecPuissances[i+1] - vecPuissances[i]));
	}

	cout << *min_element(vecDiffPuissance.begin(), vecDiffPuissance.end()) <<endl;
	
	return 0;
}