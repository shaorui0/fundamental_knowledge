
#include <stdio.h> 
#include <stdlib.h> 
  
int main() 
{ 
  
    // This pointer will hold the 
    // base address of the block created 
    int* ptr; 
    long n, i; 
  
    // Get the number of elements for the array 
    //n = 5; 
    n = 0x40000000; //4GB
    printf("Enter number of elements: %ld\n", n); 
  
    // Dynamically allocate memory using malloc() 
    ptr = (int*)malloc(n * sizeof(int)); //4GB * 4
  
    // Check if the memory has been successfully 
    // allocated by malloc or not 
    if (ptr == NULL) { 
        printf("Memory not allocated.\n"); 
        exit(0); 
    } 
    else { 
  
        // Memory has been successfully allocated 
        printf("Memory successfully allocated using malloc.\n"); 
  
        // Get the elements of the array 
        for (i = 0; i < n; ++i) { 
            ptr[i] = i + 1; 
        } 
  
        // Print the elements of the array 
        printf("The elements of the array are: "); 
        for (i = 0; i < n; ++i) { 
            printf("%d, ", ptr[i]); 
        } 


        // Do not forget to free memory
        free(ptr);
    } 
  
    return 0; 
} 