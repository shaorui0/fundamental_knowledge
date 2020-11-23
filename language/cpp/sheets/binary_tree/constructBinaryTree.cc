#include <string.h>
#include <string>
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

struct BinaryTreeNode
{
    int data;
    BinaryTreeNode* left = NULL;
    BinaryTreeNode* right = NULL;

};

void printBinaryTree(BinaryTreeNode* root)
{
    //check root is not null
    if (root == NULL) {
        return;
    }
    //init a queue
    queue<BinaryTreeNode*> aQueue;
    //queue.push(root)
    aQueue.push(root);
    while (!aQueue.empty()) {
        BinaryTreeNode* firstNode = aQueue.front();
        aQueue.pop();//will be dead loop if forget pop

        cout << firstNode->data << "\t";

        BinaryTreeNode* leftNode = firstNode->left;
        if (leftNode != NULL){
            aQueue.push(leftNode);
        }
        BinaryTreeNode* rightNode = firstNode->right;
        if (rightNode != NULL){
            aQueue.push(rightNode);
        }
    }
    return;
}

void printIntList(int* preLeft, int* preRight)
{
    if (preLeft == NULL || preRight == NULL || preRight < preLeft){
        return;
    }
    int* tmp = preLeft;
    while (tmp < preRight){
        cout << tmp[0] << "\t";
        tmp++;
    }
    cout << preRight[0];
    cout << endl;
}

BinaryTreeNode* constructCore(int* preLeft,
                    int* preRight,
                    int* midLeft,
                    int* midRight)
{
    cout << "current: "<<endl;
    printIntList(preLeft,preRight);
    printIntList(midLeft,midRight);

    //get preorder_start_node value
    int rootValue = *preLeft;
    BinaryTreeNode* root = new BinaryTreeNode();
    root->data = *preLeft;
    root->left = NULL;
    root->right = NULL;
    //init a node that value equal to the value

    //[leaf] if preorder_start_node and preoder_end_node are equals
    if (preLeft == preRight){
        if (midLeft == midRight && preLeft[0] == midLeft[0]){
            return root;
        }
        else{
            cout << "Invalid input" << endl;
            return NULL;
        }
    }
    //找到root在中序数的index, 计算出左子树长度
    //find index of root in inorder

    //tmp_inorder_start_node = inorder_start_node
    int* tmp = midLeft;
    while (tmp < midRight && tmp[0] != rootValue){
        tmp++;
    }
    //while tmp_inorder_start_node < inorder_end_node
    //        && tmp_inorder_start_node value not equal value of root data:
    //    tmp to next

    //get length of left tree
    int lenLeftTree = tmp - midLeft;
    cout << ">>> " << lenLeftTree << endl;

    //lenLeftTree = tmp_inorder_start_node - inorder_start_node
    
    //递归左, 条件左子树的长度 > 0
    if (lenLeftTree > 0) {
        root->left = constructCore(
            preLeft + 1,
            preLeft + lenLeftTree,
            midLeft,
            midLeft + lenLeftTree - 1
        );
    }


    //递归右，条件：右子树的长度 > 0
    if (lenLeftTree < preRight - preLeft) {
        root->right = constructCore(
            preLeft + lenLeftTree + 1,
            preRight,
            midLeft + lenLeftTree + 1,
            midRight
        );
    }
    return root;
}

BinaryTreeNode* construct(int* preLeft,
                    int* midLeft,
                    int len)
{
    //check edge
    cout << "len: " << len << endl;
    return constructCore(preLeft, preLeft+len-1, midLeft, midLeft+len-1);
}

int main()
{
    BinaryTreeNode* a = new BinaryTreeNode();
    BinaryTreeNode* b = new BinaryTreeNode();
    BinaryTreeNode* c = new BinaryTreeNode();
    BinaryTreeNode* d = new BinaryTreeNode();
    BinaryTreeNode* e = new BinaryTreeNode();
    BinaryTreeNode* f = new BinaryTreeNode();
    a->data = 1;
    b->data = 2;
    c->data = 3;
    d->data = 4;
    a->left = b;
    a->right = d;
    b->right = c;
    printBinaryTree(a);


    //init two list
    //vector<int> aList = {1, 2, 4, 7, 3, 5, 6, 8};
    //vector<int> bList = {4, 7, 2, 1, 5, 3, 8, 6};
    int aList[] = {1, 2, 4, 7, 3, 5, 6, 8};
    int bList[] = {4, 7, 2, 1, 5, 3, 8, 6};
    BinaryTreeNode* root = construct(aList, bList, 8);
    printBinaryTree(root);
    //cout << construct(aList, bList, 8) << endl;
    return 0;
}
