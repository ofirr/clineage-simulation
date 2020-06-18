function [ newChildrenLifeTokens ] = FuncUpdateChildrenLifeTokens( ChildrenLifeTokens, T, Nodes, parentType, rnd, rep )
%disp('life tokens');
%disp(ChildrenLifeTokens);
rtl = rand;
p = exprnd(0.2);
my_token = ChildrenLifeTokens(rep);
left_child_token = round(my_token*p);
right_child_token = my_token - left_child_token;

if rtl > 0.5
    newChildrenLifeTokens = [right_child_token, left_child_token];
else
    newChildrenLifeTokens = [left_child_token, right_child_token];
end
end
