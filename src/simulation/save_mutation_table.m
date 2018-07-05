function [] = save_mutation_table(path_mutation_table, mutation_table)

% write mutation table to a file
switch class(mutation_table)

    case 'table'

        writetable(...
            mutation_table, ...
            path_mutation_table, ...
            'WriteVariableNames', true, ...
            'WriteRowNames', true, ...
            'Delimiter', 'tab' ...
        );

    case 'cell'

        % open a file
        file_out = fopen(path_mutation_table, 'w');

        % iterate through rows in the mutation table
        for row = 1:size(mutation_table, 1)
            % convert a row in the cell array to a string array
            line = strings(1, size(mutation_table, 2));
            for col = 1:size(mutation_table, 2)
                switch class( mutation_table{row, col} )
                    case 'char'
                        line(col) = string(mutation_table(row, col));
                    case 'cell'
                        alleles = string(mutation_table{row, col}{1, 1});
                        % replace any missing to a text "NaN"
                        alleles( ismissing(alleles) ) = "NaN";
                        line(col) = strjoin(alleles, '/');
                end
                %line = string( mutation_table_final(row,:) );
            end

            % concatenate with a tab characeter
            line = strjoin( line, '\t' );
            % write to a file
            fprintf(file_out, "%s\n", line);
        end

        % close the file
        fclose(file_out);

%     case 'cell'
%
%         % open a file
%         file_out = fopen(path_mutation_table, 'w');
%
%         % iterate through rows in the mutation table
%         for row = 1:size(mutation_table, 1)
%             % convert a row in the cell array to a string array
%             line = string( mutation_table(row,:) );
%             % replace any missing to a text "NaN"
%             line( ismissing(line) ) = "NaN";
%             % concatenate with a tab characeter
%             line = strjoin( line, '\t' );
%             % write to a file
%             fprintf(file_out, "%s\n", line);
%         end
%
%         % close the file
%         fclose(file_out);

end
