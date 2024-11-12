import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Set up the initial page configuration
st.set_page_config(
     page_title='House Price Prediction',
     page_icon='🏡',
     initial_sidebar_state="expanded",
)

# Define background image CSS
page_bg_img = """
<style>
[data-testid = "stAppViewContainer"] {  
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center center;
  background-repeat: repeat;
  background-image: url("data:image/svg+xml;utf8,%3Csvg viewBox=%220 0 2000 1400%22 xmlns=%22http:%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cmask id=%22b%22 x=%220%22 y=%220%22 width=%222000%22 height=%221400%22%3E%3Cpath fill=%22url(%23a)%22 d=%22M0 0h2000v1400H0z%22%2F%3E%3C%2Fmask%3E%3Cpath fill=%22%23fff%22 d=%22M0 0h2000v1400H0z%22%2F%3E%3Cg mask=%22url(%23b)%22%3E%3Cg transform=%22rotate(5) scale(1.1)%22 style=%22transform-origin:center center%22 fill=%22%23c0c7e8%22%3E%3Ccircle cy=%2229.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%2259%22 cy=%2229.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22295%22 cy=%2229.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22590%22 cy=%2229.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22708%22 cy=%2229.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22826%22 cy=%2229.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22885%22 cy=%2229.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221003%22 cy=%2229.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221298%22 cy=%2229.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22147.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22324.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22442.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22619.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22678.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22914.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22973.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221327.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221386.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221445.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221681.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221740.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221858.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221917.5%22 cy=%2288.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22236%22 cy=%22147.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22590%22 cy=%22147.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22649%22 cy=%22147.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221003%22 cy=%22147.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221947%22 cy=%22147.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%222006%22 cy=%22147.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%2229.5%22 cy=%22206.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22147.5%22 cy=%22206.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22678.5%22 cy=%22206.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22796.5%22 cy=%22206.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22855.5%22 cy=%22206.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221032.5%22 cy=%22206.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221268.5%22 cy=%22206.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221445.5%22 cy=%22206.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221563.5%22 cy=%22206.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221976.5%22 cy=%22206.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%2259%22 cy=%22265.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22649%22 cy=%22265.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22826%22 cy=%22265.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22885%22 cy=%22265.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22944%22 cy=%22265.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221062%22 cy=%22265.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221121%22 cy=%22265.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221180%22 cy=%22265.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221829%22 cy=%22265.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%2229.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%2288.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22147.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22206.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22383.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22737.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221091.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221209.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221504.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221563.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221681.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221740.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221799.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221917.5%22 cy=%22324.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22177%22 cy=%22383.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22236%22 cy=%22383.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22413%22 cy=%22383.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221062%22 cy=%22383.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221180%22 cy=%22383.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221652%22 cy=%22383.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221711%22 cy=%22383.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221770%22 cy=%22383.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%222006%22 cy=%22383.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22265.5%22 cy=%22442.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22796.5%22 cy=%22442.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22855.5%22 cy=%22442.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221268.5%22 cy=%22442.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221386.5%22 cy=%22442.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221445.5%22 cy=%22442.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221622.5%22 cy=%22442.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221858.5%22 cy=%22442.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221917.5%22 cy=%22442.5%22 r=%224.4%22%2F%3E%3Ccircle cy=%22501.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22295%22 cy=%22501.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22354%22 cy=%22501.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22472%22 cy=%22501.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22649%22 cy=%22501.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221003%22 cy=%22501.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221180%22 cy=%22501.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221770%22 cy=%22501.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221947%22 cy=%22501.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%222006%22 cy=%22501.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22147.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22324.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22383.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22501.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22737.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221032.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221327.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221386.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221445.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221681.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221740.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221799.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221858.5%22 cy=%22560.5%22 r=%224.4%22%2F%3E%3Ccircle cy=%22619.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22236%22 cy=%22619.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22354%22 cy=%22619.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22531%22 cy=%22619.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22590%22 cy=%22619.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221003%22 cy=%22619.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221239%22 cy=%22619.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221298%22 cy=%22619.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221416%22 cy=%22619.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221475%22 cy=%22619.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221888%22 cy=%22619.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22147.5%22 cy=%22678.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22324.5%22 cy=%22678.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22501.5%22 cy=%22678.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221032.5%22 cy=%22678.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221091.5%22 cy=%22678.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221268.5%22 cy=%22678.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221386.5%22 cy=%22678.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221504.5%22 cy=%22678.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221681.5%22 cy=%22678.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22177%22 cy=%22737.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22236%22 cy=%22737.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22354%22 cy=%22737.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22767%22 cy=%22737.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22826%22 cy=%22737.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22885%22 cy=%22737.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221180%22 cy=%22737.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221239%22 cy=%22737.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221298%22 cy=%22737.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221652%22 cy=%22737.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221888%22 cy=%22737.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22501.5%22 cy=%22796.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22560.5%22 cy=%22796.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22678.5%22 cy=%22796.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22855.5%22 cy=%22796.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22914.5%22 cy=%22796.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221032.5%22 cy=%22796.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221268.5%22 cy=%22796.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221327.5%22 cy=%22796.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221504.5%22 cy=%22796.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221858.5%22 cy=%22796.5%22 r=%224.4%22%2F%3E%3Ccircle cy=%22855.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22413%22 cy=%22855.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22708%22 cy=%22855.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22767%22 cy=%22855.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22944%22 cy=%22855.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221003%22 cy=%22855.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221062%22 cy=%22855.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221357%22 cy=%22855.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221711%22 cy=%22855.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22206.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22324.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22383.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22442.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22619.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22914.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221091.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221268.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221386.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221504.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221563.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221622.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221681.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221799.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221976.5%22 cy=%22914.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22413%22 cy=%22973.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22649%22 cy=%22973.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22826%22 cy=%22973.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221121%22 cy=%22973.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221534%22 cy=%22973.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%222006%22 cy=%22973.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22147.5%22 cy=%221032.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22383.5%22 cy=%221032.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22560.5%22 cy=%221032.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22737.5%22 cy=%221032.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22914.5%22 cy=%221032.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221091.5%22 cy=%221032.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221268.5%22 cy=%221032.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221445.5%22 cy=%221032.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221681.5%22 cy=%221032.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221799.5%22 cy=%221032.5%22 r=%224.4%22%2F%3E%3Ccircle cy=%221091.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22354%22 cy=%221091.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22472%22 cy=%221091.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221003%22 cy=%221091.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221121%22 cy=%221091.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221239%22 cy=%221091.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221298%22 cy=%221091.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221357%22 cy=%221091.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221416%22 cy=%221091.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221534%22 cy=%221091.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221770%22 cy=%221091.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221947%22 cy=%221091.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22206.5%22 cy=%221150.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22265.5%22 cy=%221150.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22619.5%22 cy=%221150.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22678.5%22 cy=%221150.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221150.5%22 cy=%221150.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221386.5%22 cy=%221150.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221445.5%22 cy=%221150.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221740.5%22 cy=%221150.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221799.5%22 cy=%221150.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221976.5%22 cy=%221150.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22649%22 cy=%221209.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221062%22 cy=%221209.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221416%22 cy=%221209.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221652%22 cy=%221209.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221888%22 cy=%221209.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22383.5%22 cy=%221268.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22442.5%22 cy=%221268.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22737.5%22 cy=%221268.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22796.5%22 cy=%221268.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221386.5%22 cy=%221268.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221681.5%22 cy=%221268.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221917.5%22 cy=%221268.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221976.5%22 cy=%221268.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22177%22 cy=%221327.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221121%22 cy=%221327.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221357%22 cy=%221327.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221475%22 cy=%221327.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221829%22 cy=%221327.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221947%22 cy=%221327.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%2288.5%22 cy=%221386.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22265.5%22 cy=%221386.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22560.5%22 cy=%221386.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22737.5%22 cy=%221386.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22796.5%22 cy=%221386.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%22914.5%22 cy=%221386.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221386.5%22 cy=%221386.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221622.5%22 cy=%221386.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221681.5%22 cy=%221386.5%22 r=%224.4%22%2F%3E%3Ccircle cx=%221799.5%22 cy=%221386.5%22 r=%224.4%22%2F%3E%3C%2Fg%3E%3C%2Fg%3E%3Cdefs%3E%3CradialGradient id=%22a%22%3E%3Cstop offset=%2232.8%25%22 stop-color=%22%23fff%22 stop-opacity=%220%22%2F%3E%3Cstop offset=%22100%25%22 stop-color=%22%23fff%22 stop-opacity=%22.672%22%2F%3E%3C%2FradialGradient%3E%3C%2Fdefs%3E%3C%2Fsvg%3E");
}


</style>
"""
# Apply the background image
st.markdown(page_bg_img, unsafe_allow_html=True)

# Sidebar with information about Bangalore
st.sidebar.title("🌆 About Bangalore")

# Adding an image of Bangalore to the sidebar
st.sidebar.image("1.jpg", caption="Bangalore City", use_container_width=True)

# Adding a description about Bangalore
st.sidebar.markdown("""
Bangalore, officially known as Bengaluru, is the capital city of the Indian state of Karnataka. 
Known as the "Silicon Valley of India," Bangalore is the leading information technology (IT) hub of the country. 

🌟 **Quick Facts about Bangalore:**
- **State:** Karnataka
- **Nicknames:** Garden City, Silicon Valley of India
- **Population:** Over 12 million
- **Weather:** Mild, with moderate rainfall and pleasant climate year-round

Bangalore is home to numerous startups, IT companies, educational institutions, and vibrant cultural events. 
With its blend of modernity and tradition, it attracts people from all over the world to live, work, and study.
""")

# Display a welcome toast only when the webpage is reloaded
if 'welcome_toast' not in st.session_state:
    st.session_state['welcome_toast'] = True
    st.toast('WELCOME!', icon='🙏')

# Load model and data
with open("RidgeModel.pkl", 'rb') as file:
    model = pickle.load(file)

# Load the cleaned data to get unique locations
data = pd.read_csv("cleaned_data.csv")
locations = sorted(data['location'].unique())

# Streamlit app layout
# Expansive title and introductory description
st.markdown("""
    <h1 style='text-align: center; font-size: 3em;'>🏙️ Silicon City House Price Prediction App </h1>
""", unsafe_allow_html=True)

st.write("Welcome to the house price prediction tool. Enter the details of the property to predict the price.")

# User inputs
location = st.selectbox("Select Location", locations)
total_sqft = st.number_input("Total Square Feet", min_value=0)
bath = st.number_input("Number of Bathrooms", min_value=1, max_value=10, step=1)
bhk = st.number_input("Number of Bedrooms (BHK)", min_value=1, max_value=10, step=1)

# Predict button
if st.button("🔮Predict Price"):
    # Prepare input for the model
    input_data = pd.DataFrame([[location, total_sqft, bath, bhk]], columns=['location', 'total_sqft', 'bath', 'bhk'])

    # Prediction
    prediction = model.predict(input_data)[0]
    st.success(f"🏡 **Estimated House Price:** ₹ {np.round(prediction, 2)}💸")
