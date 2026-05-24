% MATLAB Program to simulate a 1D Kalman Filter with LIDAR measurements
clc
clear
close all

% Define parameters
num_steps = 20;  % Number of steps

% State transition matrix for constant velocity model
A = 1;
B = 1;
C= -1;

% Process noise covariance
Q = 0.8;

% Measurement noise covariance
R = 0.12;

% Initial state estimate
x = 2;          % Initial position 2 meters, initial velocity 0
x_real = x;
u = 0.5;

% Initial error covariance
P = 0.0;

%Marker Pose
m = 30;


% Storage for covariances and states
X_real=zeros(num_steps,1);
P_predicted = zeros(num_steps,1);
Z_predicted = zeros(num_steps,1);
P_updated = zeros(num_steps,1);
positions = zeros(num_steps,1);
measurements = zeros(num_steps,1);
predicted_positions = zeros(num_steps,1);
predicted_meas_positions = zeros(num_steps,1);

% Simulate the Kalman Filter
for k = 1:num_steps
    x_real = A * x_real + B * u;

    % Prediction step
    x_pred = A * x + B * u;
    P_pred = A * P * A' + Q;
    
     % Measurement (LIDAR)
     z = (m - x_real) + (R-0.01) * abs(randn);  % Simulated measurement with noise
    
     % Observation model
     h = m-x_pred;

     % Kalman gain
     K = P_pred*C/(C*P_pred*C+ R);
   
     % Update step
     x = x_pred + K * (z - h);
     P = (1 - K*C) * P_pred;

    % Store covariances and states
    P_predicted(k) = P_pred;
    X_real(k)=x_real;
    Z_predicted(k) = R;
    P_updated(k) = P;
    positions(k) = x;
    measurements(k) = z;
    predicted_positions(k) = x_pred;
    predicted_meas_positions(k) = m-h;
end



% Plotting the robot's position and measurements
figure(2);
hold on;
grid on;
xlim([X_real(1)-5 max(X_real(num_steps)+2,m+2)]);
ylim([-0.5 1.5]);
xlabel('Position');
ylabel('PDF');
title('Robot Position and Measurements over Time');


for k = 1:num_steps
    % Clear previous plots
    cla;
    
    %plot Wall
    xline(m, 'k-', 'Wall', 'LineWidth', 5, 'DisplayName', 'Wall');

    %plot Floor
    yline(0, 'k-', 'Floor', 'LineWidth', 5, 'DisplayName', 'Floor');

    %Plot Real robot
    body_width = 1;
    body_height = 0.1;
    rectangle('Position', [X_real(k)-body_width/2, 0.05, body_width, body_height], 'FaceColor', [0.8, 0.8, 0.8]);
    rectangle('Position', [X_real(k), 0.15, body_width/2, body_height/2], 'FaceColor', [0.8, 0.8, 0.8]);

    rectangle('Position',[X_real(k)+body_width/8, 0.00, body_width, body_height],'Curvature',[1 1],'FaceColor', [0.8, 0.8, 0.8])
    rectangle('Position',[X_real(k)-body_width, 0.00, body_width, body_height],'Curvature',[1 1],'FaceColor', [0.8, 0.8, 0.8])

    % Plot the measurements
    plot([positions(k),positions(k)+measurements(k)], [0.18, 0.18], 'DisplayName', 'Measurement', 'LineWidth', 3);

    % Plot the current position as a triangle
    plot(positions(k),-0.1, 'b^', 'MarkerSize', 20, 'DisplayName', 'Current Updated Position', 'LineWidth', 2);
    plot(predicted_positions(k),-0.1, 'r^', 'MarkerSize', 20, 'DisplayName', 'Current Predicted Position','LineWidth', 2);
    
    % Gaussian bell curves for predicted and updated variances
    x_range = linspace(positions(k) - 200 * sqrt(P_updated(k)), positions(k) + 200 * sqrt(P_updated(k)), 10000);

    pred_gauss = exp(-0.5 * ((x_range - predicted_positions(k)) / sqrt(P_predicted(k))).^2) / (sqrt(2 * pi) * sqrt(P_predicted(k)));
    meas_gauss = exp(-0.5 * ((x_range - predicted_meas_positions(k)) / sqrt(Z_predicted(k))).^2) / (sqrt(2 * pi) * sqrt(Z_predicted(k)));
    updated_gauss = exp(-0.5 * ((x_range - positions(k)) / sqrt(P_updated(k))).^2) / (sqrt(2 * pi) * sqrt(P_updated(k)));
    
    % Normalize for better visualization
    %pred_gauss = pred_gauss * max(ylim) / max(pred_gauss);
    %meas_gauss = meas_gauss * max(ylim) / max(meas_gauss);
    %updated_gauss = updated_gauss * max(ylim) / max(updated_gauss);
    
    plot(x_range, pred_gauss, 'r--', 'DisplayName', 'Predicted Variance Gaussian','LineWidth', 2);
    plot(x_range, meas_gauss, 'g--', 'DisplayName', 'Predicted Measurement Variance Gaussian', 'LineWidth', 2);
    plot(x_range, updated_gauss, 'b--', 'DisplayName', 'Updated Variance Gaussian','LineWidth', 2);
    
    % Update plot
    drawnow;
    legend('show');

    pause(0.1);
end

% Plotting the error covariances
figure(1);
x_range = 1:1:num_steps;
plot(x_range, P_predicted, 'r', 'DisplayName', 'Predicted Position Variance','LineWidth', 2);
hold on;
plot(x_range, P_updated, 'b', 'DisplayName', 'Updated Position Variance','LineWidth', 2);
plot(x_range, Z_predicted, 'g', 'DisplayName', 'Observation model Position Variance','LineWidth', 2);
xlabel('Time Step');
ylabel('Position Variance');
legend;
title('Position Variance over Time');



