%fitting for Kittel formular
%(3)
% FIELD Oe, frequency Hz

% clear;field=[];frequency=[];
ff2=@(beta2,x)1.76*10^7/(2.*pi).*((x).*(x+beta2)).^(1/2);
fitoptions2=optimset('Display','off');
beta20=1;
beta2=lsqcurvefit(ff2,beta20,field,frequency,[],[],fitoptions2);
figure;plot(field,frequency,'b.');
hold on;plot(linspace(0,field(end),1000),ff2(beta2,linspace(0,field(end),1000)),'r.');legend('experiment','fitting');xlabel('B(KG)');ylabel('f(Hz)');title('Kittel formula')
title(['4PiM_eff =' num2str(beta2) '(KG)'])
%set(gcf,'Units','centimeters','Position',[5,5,10.16,8.89]);
disp(['4PiM_eff =' num2str(beta2) '(Oe)'])

%output to origin
output_M_eff1=[field,frequency];
output_M_eff2=[linspace(0,field(end),1000)',ff2(beta2,linspace(0,field(end),1000))'];