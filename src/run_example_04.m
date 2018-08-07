run1 = load(fullfile('../examples/example-early-stop-verification/', 'outputs-all-the-way', 'workspace.mat'), 'my_run');
run2 = load(fullfile('../examples/example-early-stop-verification/', 'outputs-early-stop', 'workspace.mat'), 'my_run');

[result, reasons] = are_runs_identical(run1.my_run, run2.my_run);

fprintf("Result: %d\n", result);
disp("Reasons:");
disp(reasons);
