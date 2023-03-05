%fitting for Gilbert damping 
% saitoh's formula
% Oe vs Hz
% clear;frequency=[];half_linewidth=[]
ffitupvalue=12e9;
gamma=1.76*10^10;
figure;plot(frequency,half_linewidth,'o')
%fitoptions3=optimset('Display','off');
[malpha,malpha_confidence_interval]=regress(half_linewidth,[frequency,ones(size(frequency,1),1)],0.05);

hold on;x=linspace(0,ffitupvalue,1000);plot(x,polyval(malpha,x),'r.');legend('experiment','fitting');xlabel('f(Hz)');ylabel('\mu_{0} \Delta H (KG)');title('fitting for Gilbert damping')

%set(gcf,'Units','centimeters','Position',[5,5,10.16,8.89]);
disp(['Gelbert damping =' num2str(malpha(1)*gamma/(2*pi)/1000)])
disp(['Gelbert damping delta=' num2str((malpha(1)-malpha_confidence_interval(1))*gamma/(2*pi)/1000)])


%output to origin
output_frequency_deltaM=[frequency,(half_linewidth)];
output_frequency_deltaM2=[x',polyval(malpha,x)'];

