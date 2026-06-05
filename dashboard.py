import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import os
# OpenCV import is moved to Live Feed section for headless environment support

st.set_page_config(
    page_title='AI Automotive Safety Dashboard',
    page_icon='🚦',
    layout='wide',
    initial_sidebar_state='expanded'
)

theme = st.sidebar.radio('Theme', ['Light', 'Dark'], index=0)

is_dark = theme == 'Dark'
page_bg = 'linear-gradient(135deg, #081021 0%, #131d38 100%)' if is_dark else 'linear-gradient(135deg, #f8fafc 0%, #e8f4f8 100%)'
content_bg = '#111827' if is_dark else 'rgba(255, 255, 255, 0.98)'
text_color = '#f8fafc' if is_dark else '#0f172a'
card_bg = 'rgba(22, 34, 57, 0.95)' if is_dark else 'rgba(255, 255, 255, 0.95)'
border_color = 'rgba(248, 250, 252, 0.12)' if is_dark else 'rgba(15, 23, 42, 0.08)'
button_text = '#f8fafc' if is_dark else '#0f172a'
plot_font_color = text_color

page_css = f'''
<style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}
html, body, .stApp {{
    background: {page_bg};
    color: {text_color};
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}
.block-container {{
    max-width: 1600px;
    padding-top: 2.5rem;
    padding-bottom: 2.5rem;
    background: {content_bg};
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0f3460 0%, #163a5f 50%, #1e4976 100%) !important;
    border-right: 1px solid rgba(0, 212, 255, 0.15);
}}
.stApp [data-testid="stSidebar"] * {{
    color: #ffffff !important;
}}
.stApp .main *,
.stApp .block-container * {{
    color: {text_color} !important;
}}
.gradient-header *,
.hero *,
.footer-premium * {{
    color: #ffffff !important;
}}
.stButton > button {{
    background: linear-gradient(135deg, #00d4ff 0%, #0084d4 100%);
    color: {button_text} !important;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: 600;
}}
.info-card {{
    background: {card_bg};
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(15, 52, 96, 0.08);
    border: 1px solid {border_color};
}}
.footer-premium {{
    background: linear-gradient(135deg, #0f3460 0%, #163a5f 100%);
    color: rgba(255, 255, 255, 0.9);
    text-align: center;
    padding: 32px 20px;
    border-radius: 16px;
    margin-top: 48px;
}}
</style>
'''

st.markdown(page_css, unsafe_allow_html=True)

with st.sidebar:
    st.markdown('### AI AUTOMOTIVE SAFETY')
    st.markdown('---')
    selected_page = st.radio(
        'Navigation',
        ['Dashboard', 'Analytics', 'Alerts', 'Live Feed', 'Settings', 'Data Export'],
        index=0
    )
    st.markdown('---')
    st.markdown('### System Status')
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Status', 'Online', delta_color='off')
    with col2:
        st.metric('Connection', 'Active', delta_color='off')
    st.markdown('---')
    st.markdown('### Quick Stats')
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Vehicles', '247', '12 today')
    with col2:
        st.metric('Alerts', '8', '-2 last hour')
    st.markdown('---')
    st.info('Tip: Use the sidebar to switch between dashboard sections.')

if selected_page == 'Dashboard':
    st.markdown('''
    <div style="background: linear-gradient(135deg, #0f3460 0%, #20c997 100%); border-radius: 18px; padding: 32px; color: white; box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);">
        <h1 style="margin-bottom: 8px;">AI Automotive Safety Dashboard</h1>
        <p style="margin: 0; font-size: 1.05rem;">Real-time vehicle detection, traffic monitoring, and safety analytics.</p>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('## Real-Time Metrics')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Active Cameras', '2', 'Online')
    with col2:
        st.metric('Vehicles Detected', '247', '15 today')
    with col3:
        st.metric('Average Density', '45%', '-5%')
    with col4:
        st.metric('Safety Alerts', '8', '-2')

    st.markdown('---')
    st.markdown('## Analytics & Insights')
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Vehicle Detection Over Time')
        hours = pd.date_range(start=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), periods=24, freq='h')
        vehicle_counts = np.random.randint(100, 300, 24)
        detection_df = pd.DataFrame({'Time': hours, 'Vehicles': vehicle_counts})
        fig = px.line(detection_df, x='Time', y='Vehicles', markers=True, title='24-Hour Detection Trend')
        fig.update_traces(line_color='#00d4ff', marker_size=8)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified',
            font=dict(color=plot_font_color),
            title=dict(font=dict(color=plot_font_color)),
            xaxis=dict(title_font=dict(color=plot_font_color), tickfont=dict(color=plot_font_color)),
            yaxis=dict(title_font=dict(color=plot_font_color), tickfont=dict(color=plot_font_color)),
            legend=dict(font=dict(color=plot_font_color))
        )
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.markdown('### Traffic Density Distribution')
        density_categories = ['Low', 'Medium', 'High', 'Critical']
        density_values = [15, 35, 40, 10]
        fig = px.pie(values=density_values, names=density_categories, color_discrete_sequence=['#20c997', '#ffc107', '#ff9800', '#dc3545'], title='Current Traffic Density')
        fig.update_traces(textposition='auto', textfont_color=plot_font_color)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=plot_font_color),
            title=dict(font=dict(color=plot_font_color)),
            legend=dict(font=dict(color=plot_font_color))
        )
        st.plotly_chart(fig, width='stretch')

    st.markdown('---')
    st.markdown('## Recent Detections')
    detection_data = {
        'Time': pd.date_range(start=datetime.now().replace(hour=10, minute=0, second=0, microsecond=0), periods=10, freq='5min'),
        'Vehicle Type': ['Car', 'Truck', 'Bus', 'Car', 'Motorcycle', 'Truck', 'Car', 'Car', 'Bus', 'Car'],
        'Confidence': [0.95, 0.88, 0.92, 0.97, 0.85, 0.90, 0.93, 0.96, 0.89, 0.94],
        'Status': ['Safe', 'Warning', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Warning', 'Safe']
    }
    detection_table = pd.DataFrame(detection_data)
    st.dataframe(detection_table, width='stretch', hide_index=True)

    st.markdown('---')
    st.markdown('## System Information')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('### Device Info')
        st.markdown('**Engine:** Computer Vision Engine<br>**Processor:** Intel i7<br>**GPU:** NVIDIA CUDA', unsafe_allow_html=True)
    with col2:
        st.markdown('### Detection Model')
        st.markdown('**Model:** YOLOv3<br>**Framework:** OpenCV<br>**Classes:** 80 objects', unsafe_allow_html=True)
    with col3:
        st.markdown('### Performance')
        st.markdown('**FPS:** 30<br>**Latency:** 45ms<br>**Uptime:** 15h 42m', unsafe_allow_html=True)

elif selected_page == 'Analytics':
    st.markdown('## Detailed Analytics & Reports')
    st.markdown('### Traffic Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Total Vehicles', '2,847', '315 today', delta_color='off')
    with col2:
        st.metric('Peak Hour', '14:30 - 15:30', '487 vehicles')
    with col3:
        st.metric('Detection Confidence', '92.3%', '0.8%')
    st.markdown('---')
    st.subheader('7-Day Traffic Trend')
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    vehicles = [2400, 2800, 2200, 3000, 2847, 1800, 1200]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=days, y=vehicles, name='Vehicles', marker_color='#00d4ff', text=vehicles, textposition='auto'))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=plot_font_color),
        title=dict(font=dict(color=plot_font_color)),
        xaxis=dict(title_font=dict(color=plot_font_color), tickfont=dict(color=plot_font_color)),
        yaxis=dict(title_font=dict(color=plot_font_color), tickfont=dict(color=plot_font_color)),
        legend=dict(font=dict(color=plot_font_color)),
        hovermode='x unified'
    )
    st.plotly_chart(fig, width='stretch')
    st.markdown('---')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Vehicle Type Breakdown')
        vehicle_types = ['Sedan', 'SUV', 'Truck', 'Bus', 'Motorcycle', 'Other']
        type_counts = [520, 340, 280, 150, 90, 80]
        fig = px.bar(x=vehicle_types, y=type_counts, title='Vehicles by Type', labels={'x': 'Vehicle Type', 'y': 'Count'}, color_discrete_sequence=['#00d4ff'] * len(vehicle_types))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=plot_font_color),
            title=dict(font=dict(color=plot_font_color)),
            xaxis=dict(title_font=dict(color=plot_font_color), tickfont=dict(color=plot_font_color)),
            yaxis=dict(title_font=dict(color=plot_font_color), tickfont=dict(color=plot_font_color)),
            legend=dict(font=dict(color=plot_font_color))
        )
        st.plotly_chart(fig, width='stretch')
    with col2:
        st.subheader('Detection Confidence Distribution')
        confidence_ranges = ['80-85%', '85-90%', '90-95%', '95-100%']
        confidence_counts = [120, 280, 1050, 1397]
        fig = px.bar(x=confidence_ranges, y=confidence_counts, title='Detection Accuracy Distribution', labels={'x': 'Confidence Range', 'y': 'Count'}, color_discrete_sequence=['#ffc107', '#ff9800', '#2196f3', '#4caf50'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=plot_font_color),
            title=dict(font=dict(color=plot_font_color)),
            xaxis=dict(title_font=dict(color=plot_font_color), tickfont=dict(color=plot_font_color)),
            yaxis=dict(title_font=dict(color=plot_font_color), tickfont=dict(color=plot_font_color)),
            legend=dict(font=dict(color=plot_font_color))
        )
        st.plotly_chart(fig, width='stretch')

elif selected_page == 'Alerts':
    st.markdown('## Safety Alerts & Incidents')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Critical', '2', 'Today')
    with col2:
        st.metric('Warnings', '6', 'Today')
    with col3:
        st.metric('Info', '12', 'Today')
    with col4:
        st.metric('Resolved', '18', 'Today')
    st.markdown('---')
    alert_filter = st.selectbox('Filter Alerts', ['All', 'Critical', 'Warning', 'Info', 'Resolved'])
    st.markdown('### Recent Alerts')
    alerts_data = {
        'Time': ['14:32', '14:28', '14:15', '13:58', '13:45'],
        'Type': ['Warning', 'Warning', 'Info', 'Warning', 'Resolved'],
        'Description': [
            'High traffic density detected near intersection',
            'Vehicle detected in wrong lane',
            'System performing scheduled backup',
            'Unusual object detected on road',
            'Speeding vehicle incident resolved'
        ],
        'Severity': ['Medium', 'Medium', 'Low', 'High', 'Medium'],
        'Action': ['Review', 'Monitor', 'Ignore', 'Report', 'Archived']
    }
    alerts_df = pd.DataFrame(alerts_data)
    st.dataframe(alerts_df, width='stretch', hide_index=True)
    st.markdown('---')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Hourly Alert Trend')
        hours = list(range(0, 24))
        alert_counts = np.random.randint(0, 8, 24)
        fig = px.area(x=hours, y=alert_counts, title='Alerts Generated by Hour', labels={'x': 'Hour of Day', 'y': 'Alert Count'})
        fig.update_traces(fillcolor='rgba(220, 53, 69, 0.2)', line_color='#dc3545')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=plot_font_color),
            title=dict(font=dict(color=plot_font_color)),
            xaxis=dict(title_font=dict(color=plot_font_color), tickfont=dict(color=plot_font_color)),
            yaxis=dict(title_font=dict(color=plot_font_color), tickfont=dict(color=plot_font_color)),
            legend=dict(font=dict(color=plot_font_color))
        )
        st.plotly_chart(fig, width='stretch')
    with col2:
        st.subheader('Alert Severity Distribution')
        severity = ['Critical', 'High', 'Medium', 'Low']
        severity_counts = [2, 5, 18, 35]
        colors = ['#dc3545', '#ff6b6b', '#ffc107', '#28a745']
        fig = px.pie(values=severity_counts, names=severity, color_discrete_sequence=colors, title='Alerts by Severity Level')
        fig.update_traces(textposition='auto', textfont_color=plot_font_color)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=plot_font_color),
            title=dict(font=dict(color=plot_font_color)),
            legend=dict(font=dict(color=plot_font_color))
        )
        st.plotly_chart(fig, width='stretch')

elif selected_page == 'Live Feed':
    st.markdown('## Live Video Feed & Monitoring')
    st.info('Note: Live feed requires a connected camera or video stream.')

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Camera Source')
        src_input = st.text_input('Enter camera index (0) or RTSP/HTTP URL or file path', '0')
        start_btn = st.button('Start Stream')
        stop_btn = st.button('Stop Stream')
        confidence_threshold = st.slider('Confidence Threshold', 0.0, 1.0, 0.7)
        enable_tracking = st.checkbox('Enable Object Tracking', value=True)

    with col2:
        st.subheader('Stream Info')
        fps_metric = st.empty()
        res_metric = st.empty()
        status_metric = st.empty()

    st.markdown('---')

    if 'streaming' not in st.session_state:
        st.session_state.streaming = False

    if start_btn:
        st.session_state.streaming = True

    if stop_btn:
        st.session_state.streaming = False

    # Prepare model files
    model_cfg = os.path.join('models', 'yolov3.cfg')
    model_weights = os.path.join('models', 'yolov3.weights')
    names_path = os.path.join('models', 'coco.names')

    yolo_available = os.path.exists(model_cfg) and os.path.exists(model_weights) and os.path.exists(names_path)

    if not yolo_available:
        st.warning('YOLO model files not found in the models/ directory. Showing placeholder images.')

    placeholder = st.empty()

    if st.session_state.streaming:
        # Import cv2 only when needed (for headless environments)
        try:
            import cv2
        except ImportError:
            st.error('OpenCV (cv2) is not available in this environment. Live feed requires OpenCV.')
            st.session_state.streaming = False
        
        if st.session_state.streaming:  # Only proceed if cv2 imported successfully
            # Determine source
            try:
                src = int(src_input)
            except Exception:
                src = src_input

            cap = cv2.VideoCapture(src)

            net = None
            output_layers = None
            labels = []

            if yolo_available:
                labels = open(names_path).read().strip().split('\n')
                net = cv2.dnn.readNet(model_weights, model_cfg)
                layer_names = net.getLayerNames()
                try:
                    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
                except Exception:
                    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

            frames = 0
            start_time = time.time()

            while st.session_state.streaming and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frames += 1

                if yolo_available and net is not None:
                    (H, W) = frame.shape[:2]
                    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
                    net.setInput(blob)
                    layerOutputs = net.forward(output_layers)

                    boxes = []
                    confidences = []
                    classIDs = []

                    for output in layerOutputs:
                        for detection in output:
                            scores = detection[5:]
                            classID = int(np.argmax(scores))
                            confidence = float(scores[classID])

                            if confidence > confidence_threshold:
                                box = detection[0:4] * np.array([W, H, W, H])
                                (centerX, centerY, width, height) = box.astype('int')
                                x = int(centerX - (width / 2))
                                y = int(centerY - (height / 2))
                                boxes.append([x, y, int(width), int(height)])
                                confidences.append(float(confidence))
                                classIDs.append(classID)

                    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.4)

                    if len(idxs) > 0:
                        for i in idxs.flatten():
                            (x, y) = (boxes[i][0], boxes[i][1])
                            (w, h) = (boxes[i][2], boxes[i][3])
                            color = (0, 255, 0)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                            text = f"{labels[classIDs[i]]}: {confidences[i]:.2f}"
                            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Update metrics
                elapsed = time.time() - start_time if start_time else 0.001
                fps = frames / elapsed if elapsed > 0 else 0
                fps_metric.metric('FPS', f"{fps:.1f}")
                res_metric.metric('Resolution', f"{frame.shape[1]}x{frame.shape[0]}")
                status_metric.metric('Status', 'Streaming')

                # Convert and display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                placeholder.image(frame_rgb, width='stretch')

                # small sleep to yield control
                time.sleep(0.01)

            cap.release()
            status_metric.metric('Status', 'Stopped')
            st.session_state.streaming = False

elif selected_page == 'Settings':
    st.markdown('## System Settings & Configuration')
    with st.form('settings_form'):
        st.markdown('### Camera Configuration')
        col1, col2 = st.columns(2)
        with col1:
            st.number_input('Frame Rate (FPS)', 1, 120, 30)
        with col2:
            st.selectbox('Resolution', ['1920x1080', '1280x720', '640x480'])
        st.markdown('### Detection Settings')
        col1, col2 = st.columns(2)
        with col1:
            st.slider('Confidence Threshold', 0.0, 1.0, 0.7)
        with col2:
            st.slider('IoU Threshold', 0.0, 1.0, 0.45)
        st.markdown('### Alert Settings')
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox('Enable Audio Alerts', value=True)
        with col2:
            st.checkbox('Enable Email Notifications', value=False)
        st.markdown('### System Preferences')
        st.selectbox('Theme', ['Dark', 'Light', 'Auto'])
        st.selectbox('Language', ['English', 'Español', 'Français'])
        st.markdown('---')
        if st.form_submit_button('Save Settings'):
            st.success('Settings saved successfully!')

elif selected_page == 'Data Export':
    st.markdown('## Data Export & Reports')
    st.markdown('### Generate Report')
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date')
    with col2:
        end_date = st.date_input('End Date')
    report_type = st.selectbox('Report Type', ['Daily Summary', 'Weekly Report', 'Monthly Report', 'Custom Range'])
    include_data = st.multiselect('Include in Report', ['Traffic Statistics', 'Vehicle Analytics', 'Alert Logs', 'Performance Metrics', 'Camera Feeds'], default=['Traffic Statistics', 'Vehicle Analytics'])
    st.markdown('---')
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Generate PDF Report'):
            st.success('Report generated! Download ready.')
            st.info('Report_2026_06_03.pdf (2.4 MB)')
    with col2:
        if st.button('Export to CSV'):
            st.success('CSV export ready!')
            st.info('traffic_data_2026_06_03.csv (1.2 MB)')
    st.markdown('---')
    st.markdown('### Previous Reports')
    export_data = {
        'Date': ['2026-06-02', '2026-06-01', '2026-05-31', '2026-05-30'],
        'Type': ['Daily Report', 'Daily Report', 'Weekly Report', 'Daily Report'],
        'Size': ['2.3 MB', '2.4 MB', '8.1 MB', '2.2 MB'],
        'Format': ['PDF', 'PDF', 'PDF', 'CSV'],
        'Download': ['Ready', 'Ready', 'Ready', 'Ready']
    }
    export_df = pd.DataFrame(export_data)
    st.dataframe(export_df, width='stretch', hide_index=True)
    st.markdown('---')
    st.markdown('''
    <div class='footer-premium'>
        <h3>AI Automotive Safety System</h3>
        <p><strong>Version 1.0.0</strong> | Enterprise-Grade Traffic Monitoring</p>
        <p>© 2026 All Rights Reserved | Last Updated: June 3, 2026</p>
        <p>Status: <span style='color: #20c997;'>All Systems Operational</span></p>
    </div>
    ''', unsafe_allow_html=True)
