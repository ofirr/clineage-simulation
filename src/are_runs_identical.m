function [result, reasons] = are_runs_identical(run1, run2)

%% init
result = false;
reasons = [];

run1_nodes = run1.Nodes{1,1};
run2_nodes = run2.Nodes{1,1};

%% size different?
if size(run1) ~= size(run2)
    reasons = vertcat(reasons, "size different");
end

%% leaf names different?
if length({ run1_nodes.Name }) ~= length({ run2_nodes.Name })
    reasons = vertcat(reasons, "leaf names size different");
    return;
end

res = string( { run1_nodes.Name } ) ~= string( { run2_nodes.Name } );

if sum(res) ~= 0
    reasons = vertcat(reasons, "leaf name(s) different");
end

%% parent names different?
parent1 = { run1_nodes.Parent };
parent1 = parent1(2:end); % the root is an empty array, so let's skip

parent2 = { run2_nodes.Parent };
parent2 = parent2(2:end); % the root is an empty array, so let's skip

res = string(parent1) ~= string(parent2);

if sum(res) ~= 0
    reasons = vertcat(reasons, "parent name(s) different");
end


%% children different?
children1 = { run1_nodes.Children };
children2 = { run2_nodes.Children };

for ii = 1:length(children1)
    if isempty(children1{1,ii})
        if ~isempty(children2{1,ii})
            reasons = vertcat(reasons, "children different");
            break
        end
    else
        chld1 = string( children1{1,ii} );
        chld2 = string( children2{1,ii} );
        res = chld1 ~= chld2;
        if sum(res) ~= 0
            reasons = vertcat(reasons, "children different");
            break
        end
    end
end

%% internal state(s) different?
states1 = { run1_nodes.InternalStates };
states2 = { run2_nodes.InternalStates };

if length(states1) ~= length(states2)
    reasons = vertcat(reasons, "internal states size different");
end

for ii = 1:length(states1)
    % check MS
    res = states1{1,ii}.MS ~= states2{1,ii}.MS;
    if sum(res) ~= 0
        reasons = vertcat(reasons, "internal state MS different");
        break
    end
    % check Gen
    res = states1{1,ii}.Gen ~= states2{1,ii}.Gen;
    if sum(res) ~= 0
        reasons = vertcat(reasons, "internal state Gen different");
        break
    end
end

% if there are no reasons, two runs are identical
result = isempty(reasons);
