
print("784. Letter Case Permutation")
# Input: S = "a1b2"
# Output: ["a1b2","a1B2","A1b2","A1B2"]
def Letter_Case_Permutation(string):
    def dfs(total_list, index):
        if index == len(total_list):
            print(total_list)
            return total_list

        if total_list[index].isalpha():
            dfs(total_list[:], index + 1)

            total_list[index] = total_list[index].upper()
            dfs(total_list[:], index + 1) # 这里连续两次dfs和之前的for+dfs其实是一样的，也就不需要pop了

        else:
            dfs(total_list[:], index + 1)
    dfs(list(string), 0)

Letter_Case_Permutation("a1b2")
