clear all
rmat=load("MATLAB.mat");
eff=load("valid_data.mat");
error=rmat.results.error;
good_i=0;
bad_i=0;
for it=1:size(error,2)
    if abs(error(it))<10
        good_i=good_i+1;
        good(good_i)=eff.eff_list(it);
    end
    if abs(error(it))>80
        bad_i=bad_i+1;
        bad(bad_i)=eff.eff_list(it);
    end
end
