function plot_pattern3D(phi_vector,theta_vector,pattern,content_title,bar_title)
        
        [Phi,Theta] = meshgrid(phi_vector,theta_vector);
        arrow_length = 60;
        arrow_text_dist = 5;
        bar_scale = 'N';
%         pattern_null_rescale = 'Y';

%%
% pattern_span = 40;
% % % change the value range to [pattern_max-40, pattern_max]
% % if pattern_null_rescale == 'Y'
%     % to make sure the gain values are in the plot range
% %     pattern_span = 40;
%         pattern_min = min(min(pattern));
%         pattern_max = max(max(pattern));
%         if pattern_min < pattern_max-pattern_span
%             pattern_min = pattern_max-pattern_span;
%             for i = 1:length(theta_vector)
%                 for j = 1:length(phi_vector)
%                     if pattern(i,j) < pattern_min
%                     pattern(i,j) = pattern_min;
%                     end
%                 end
%             end
%         elseif pattern_min >= pattern_max-pattern_span
%             disp('Gain range is no more than 40dB');
% %             pattern(I_row, I_col) = pattern_max-pattern_span;
%             % make the range to 40 by reducing the minimum
%         end
%         pattern_min = pattern_max - pattern_span;
%         pattern = pattern - pattern_min;%*ones(size(pattern))
        % make sure only positive values in the pattern matrix
% else
        pattern_span = 40;
        [pattern_min,min_index] = min(pattern(:));
        [I_row, I_col] = ind2sub(size(pattern),min_index);
        pattern_max = max(max(pattern));
        title_pattern_max = pattern_max;
        
        if pattern_min < pattern_max-pattern_span
            pattern_min = pattern_max-pattern_span;
            for i = 1:length(theta_vector)
                for j = 1:length(phi_vector)
                    if pattern(i,j) < pattern_min
                    pattern(i,j) = pattern_min;
                    end
                end
            end
        elseif pattern_min > pattern_max-pattern_span
            pattern(I_row, I_col) = pattern_max-pattern_span;
            % make the range to 40 by reducing the minimum
        end
        pattern_min = pattern_max - pattern_span;
        pattern = pattern - pattern_min;%*ones(size(pattern))
        % make sure only positive values in the pattern matrix
% end
        
%% 
%         zlevs = linspace(minval,maxval-3,9);
%         zlevs = [zlevs maxval-0.000001];
        
        pattern_plot = pattern;
%         content_title = 'Antenna Pattern (RHCP)';
%         bar_title = 'Mag(linear)';
        r = pattern_plot.*sin(Theta);
        xm = r.*cos(Phi);
        ym = r.*sin(Phi);
        zm = pattern_plot.*cos(Theta);
        figure;
        surf(xm,ym,zm,pattern_plot,'FaceColor','interp', 'EdgeColor','none');
        grid off;
        axis off;
        Title = title ([content_title, ', ', 'Peak Gain =', ' ', num2str(title_pattern_max,'%.2f'), ' ','dBi']);
%         xlabel('xlabel'); ylabel('ylabel'); zlabel('zlabel'); 

%         vectarrow(x_axis_end_point(1,:),x_axis_end_point(2,:));
%         y_axis_end_point = [0 0 0; 0 1 0];
%         vectarrow(y_axis_end_point(1,:),y_axis_end_point(2,:));
%         z_axis_end_point = [0 0 0; 0 0 1];
%         vectarrow(z_axis_end_point(1,:),z_axis_end_point(2,:));

        set(Title,'FontSize',15);
%         view(0,90); 
        daspect([1 1 1]);
        camlight; 
        lighting phong;
        colormap jet; 
        hcb = colorbar;
        Title = title(hcb, bar_title);
        set(Title,'FontSize',15);
        

        set(gca,'FontSize',15);
        if bar_scale == 'N'
            pattern_max = 5;
            pattern_min = -35;
        end
        colorbar_resolution = 5;
        set(hcb,'Ytick',[linspace(0,pattern_span-colorbar_resolution,8) pattern_span]);
        L=cellfun(@(x)sprintf('%d',x),num2cell([linspace(pattern_min,pattern_max-colorbar_resolution,8) pattern_max]),'Un',0);
        set(hcb,'Yticklabel',L);
        
        % defnie the place of decimal
        hold all;
        x_axis_end_point = [0 0 0; arrow_length 0 0];
        y_axis_end_point = [0 0 0; 0 arrow_length 0];
        z_axis_end_point = [0 0 0; 0 0 arrow_length];
        plot.arrow(x_axis_end_point(1,:),x_axis_end_point(2,:),10,'Ends','Stop','Width',3,'FaceColor','r','EdgeColor','r');
        text(arrow_length+arrow_text_dist, 0, 0,'X');
        plot.arrow(y_axis_end_point(1,:),y_axis_end_point(2,:),10,'Ends','Stop','Width',3,'FaceColor','g','EdgeColor','g');
        text(0, arrow_length+arrow_text_dist, 0,'Y');
        plot.arrow(z_axis_end_point(1,:),z_axis_end_point(2,:),10,'Ends','Stop','Width',3,'FaceColor','b','EdgeColor','b');
        text(0, 0, arrow_length+arrow_text_dist,'Z');
        hold off;

end