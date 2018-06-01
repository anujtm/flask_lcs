from flask import Flask, request, Response, jsonify, json

app = Flask(__name__)

def check_valid_substring(substr, string_list , memoize):
    if substr in memoize:
        return memoize[substr]
        
    for i in range(1, len(string_list)):
        if substr not in string_list[i]:
            memoize[substr] = False
            return False
            
    memoize[substr] = True
    return True


def find_longest_substring(string_list):
    if len(string_list) == 1:
        return string_list
    
    # For memoizing the solution to optimize searching substring through
    # entire list
    memoize = {}
    string_list.sort(key = lambda s: len(s))
    
    smallest = string_list[0]
    
    valid_sol = set()
    # generate all possible substring for 
    # smallest word  from lagest to smallest
    # and check if it is valid solution.
    break_loop = False
    for substring_size in reversed(range(len(smallest))):
        for i in range(len(smallest) - substring_size):
            curr_substr = smallest[i: i + substring_size + 1]
            
            if (check_valid_substring(curr_substr, string_list , memoize)):
                valid_sol.add(curr_substr)
                break_loop = True
                
        if break_loop:
            break
        
    if len(valid_sol) == 0:
        # No solution was found , return empty list
        return []
    else:
        result = list(valid_sol)
        result.sort()
        #print result
        return result
    

def return_bad_request(msg):
	response = jsonify(msg)
	response.status_code = 400
	return response


@app.route("/lcs", methods = ['POST'])
def lcscall():
    json_data = request.get_json(force=True)
    
    if len(json_data) == 0:
	msg = 'No json data found. Format not acceptable'
	return return_bad_request(msg)
    
    if 'setOfStrings' not in json_data:
	msg = 'Json key setOfStrings not found. Format not acceptable'
	return return_bad_request(msg)

    if 	len(json_data['setOfStrings']) == 0:
	msg = 'setOfStrings should not be empty'
	return return_bad_request(msg)

    # Parse the json data and validate proper format
    # Make sure the key is 'value' and unique words	
    data = json_data['setOfStrings']
    unique_keys = set()
    words = []
    for el in data:
	if len(el) != 1:
		msg = 'More than one key found. Format unacceptable'
		return return_bad_request(msg)
	key = list(el.keys())[0]
	unique_keys.add(key)
	words.append(el[key])

    if len(unique_keys) != 1 or list(unique_keys)[0] != 'value':
	msg = 'Unexpected key values found. Format unacceptable'
	return return_bad_request(msg)

    if len(words) != len(set(words)):
	msg = 'Not all words are unique'
	return return_bad_request(msg)

    # all input at this point looks valid.
    solution = find_longest_substring(words)
    if len(solution) == 0:
	msg = 'No solution could be found'
	return return_bad_request(msg)
     
    resp = {'lcs' : []}
    for word_sol in solution:
		resp['lcs'].append({'value' : word_sol})
    response = jsonify(resp)
    response.status_code = 400
    return response	


if __name__ == "__main__":
    app.run(debug=True)
