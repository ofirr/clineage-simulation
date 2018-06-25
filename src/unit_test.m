run1 = load('test-run1.mat', 'my_run');
run2 = load('test-run2.mat', 'my_run');

%% identical
[result, reasons] = are_runs_identical(run1.my_run, run2.my_run);
assert( result == 1 );
assert( isempty(reasons) );

%% leaf name different
test_run = run2;
test_run.my_run.Nodes{1, 1}(1).Name = 'different name';

[result, reasons] = are_runs_identical(run1.my_run, test_run.my_run);
assert( result == 0 );
assert( reasons == "leaf name(s) different" );

%% parent name different
test_run = run2;
test_run.my_run.Nodes{1, 1}(2).Parent = 'different name';

[result, reasons] = are_runs_identical(run1.my_run, test_run.my_run);
assert( result == 0 );
assert( reasons == "parent name(s) different" );

%% children different
test_run = run2;
test_run.my_run.Nodes{1, 1}(1).Children{1,1} = 'different name';

[result, reasons] = are_runs_identical(run1.my_run, test_run.my_run);
assert( result == 0 );
assert( reasons == "children different" );

%% internal state MS different
test_run = run2;
test_run.my_run.Nodes{1, 1}(2).InternalStates.MS(1) = 1000;

[result, reasons] = are_runs_identical(run1.my_run, test_run.my_run);
assert( result == 0 );
assert( reasons == "internal state MS different" );

%% internal state Gen different
test_run = run2;
test_run.my_run.Nodes{1, 1}(2).InternalStates.Gen(1) = 777;

[result, reasons] = are_runs_identical(run1.my_run, test_run.my_run);
assert( result == 0 );
assert( reasons == "internal state Gen different" );

%% display if every assertion passes
disp("PASSED");
