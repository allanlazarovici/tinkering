#include <stdio.h>

int main()
{
    long int i, j, n, pos;
    long int golumb_first_appear[1000005], n_minus_one_first_appear;
    long int n_minus_one_num_appearances, input_number;
    char input_string[1000];

    golumb_first_appear[1] = 1;
    golumb_first_appear[2] = 2;
    golumb_first_appear[3] = 4;

    for(n=4; n<= 1000000; n++){
	/*when does n-1 first appear*/
	n_minus_one_first_appear = golumb_first_appear[n-1];

	/*How many times does n-1 appear*/
	for(i=2; i<=1000000; i++)
	    if(n-1 >= golumb_first_appear[i-1] && n-1 < golumb_first_appear[i]){
		golumb_first_appear[n] = n_minus_one_first_appear + i - 1;
		break;
	    }
    }

    while(fgets(&input_string[0], 1000, stdin) != NULL){
	sscanf(input_string, "%ld", &input_number);

	if(input_number > 0)
	    for(n=1; i<=1000000; n++)
		if(input_number >= golumb_first_appear[n] && input_number < golumb_first_appear[n+1]){
		    printf("%ld\n", n);
		    break;
		}
    }

    return 0;
}
