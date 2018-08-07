function [] = count_mutations(run, num_of_ms_loci, biallelic)

    % access to om6 microsatellite ids and repeat numbers read
    global om6_ms;

    % get initial microsatellite repeat lengths
    ms_initial = repmat(om6_ms(1:num_of_ms_loci, 2)', 1);

%{
    1;
    [2,3];
    [2,4,5];
    [2,4,6,7];
    [4,6,7,8,9];
%}
    
    % get the indexes of the leaves by extracting the last row of the LiveNodes
    leaves_idx = run.LiveNodes{end};
    
    for col = 1:length(leaves_idx)
        
        leaf_id = leaves_idx(col);

        traverse_path = [leaf_id];
        
        while true
            parent_name = run.Nodes{1,1}(leaf_id).Parent{1,1};
            parent_id = find(strcmp({run.Nodes{1,1}.Name}, parent_name));
            leaf_id = parent_id;
            traverse_path(end + 1) = leaf_id;
            if parent_id == 1 || parent_id == -1
                break;
            end
        end

        disp(traverse_path);        
        
    end

    function [str] = get_ms_repeat_length(leaf_id, biallelic, num_of_ms_loci)
        
        for locus = 1:num_of_ms_loci
        
            internal_state = run.Nodes{1,1}(leaf_id).InternalStates;

            if biallelic
                % biallelic
                switch allele
                    case 1
                        % paternal
                        ms_repeat_length = internal_state.MS1(locus);
                    case 2
                        % maternal
                        ms_repeat_length = internal_state.MS2(locus);
                    otherwise
                        error('allele must be either 1 (Paternal) or 2 (Maternal)');
                end
            else
                % monoallelic
                ms_repeat_length = internal_state.MS(locus);
            end
            
        end
        
        
    end

end
