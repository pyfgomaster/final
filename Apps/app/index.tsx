import { Button, StyleSheet, Switch, Text, View } from 'react-native';
import { useEffect, useState } from 'react';
import useSWR from 'swr';

export default function Index() {
  const [isEnabled1, setIsEnabled1] = useState(false);
  const [isEnabled2, setIsEnabled2] = useState(false);
  const [isEnabled3, setIsEnabled3] = useState(false);
  const [isEnabled4, setIsEnabled4] = useState(false);
  const SwitchEnable = () => {
    setIsEnabled1(previousState => !previousState);
    fetch('http://140.138.150.21/G14_api/ledAuto');
};
  const toggleSwitch1 = () => {
    setIsEnabled2(previousState => !previousState);
    fetch('http://140.138.150.21/G14_api/airconSwitch');
};
  const toggleSwitch2 = () => {
  setIsEnabled3(previousState => !previousState);
  fetch('http://140.138.150.21/G14_api/dehumidSwitch');
};
  const toggleSwitch3 = () => {
  setIsEnabled4(previousState => !previousState);
  fetch('http://140.138.150.21/G14_api/lightSwitch');
};
  let {data, error, mutate} = useSWR(['latest', {throwHttpErrors: true}])
  useEffect(() => {
    const interval = setInterval(() => {mutate(); }, 4000);
    return () => clearInterval(interval);
}, [mutate]);

  return (
    <View style = {styles.container}>
      <Text style = {[styles.text, {marginVertical: 10, backgroundColor: "white", padding: 10, borderRadius: 5,},]}>
        自動開關</Text>
        <Switch
          trackColor={{ false: "#767577", true: "green" }}
          thumbColor={isEnabled1 ? "#fff" : "#fff"}
          ios_backgroundColor="#3e3e3e"
          onValueChange={SwitchEnable}
          value={isEnabled1}
        />
        { !isEnabled1 &&
          (<Text style = {[styles.text, {marginVertical: 10, backgroundColor: "white", padding: 10, borderRadius: 5,},]}>
            開關空調</Text>)}
        { !isEnabled1 &&
            (<Switch
            trackColor={{ false: "#767577", true: "green" }}
            thumbColor={isEnabled2 ? "#fff" : "#fff"}
            ios_backgroundColor="#3e3e3e"
            onValueChange={toggleSwitch1}
            value={isEnabled2}
          />)}
          { !isEnabled1 &&
          (<Text style = {[styles.text, {marginVertical: 10, backgroundColor: "white", padding: 10, borderRadius: 5,},]}>
            開關除濕</Text>)}
          { !isEnabled1 &&
            (<Switch
            trackColor={{ false: "#767577", true: "green" }}
            thumbColor={isEnabled2 ? "#fff" : "#fff"}
            ios_backgroundColor="#3e3e3e"
            onValueChange={toggleSwitch2}
            value={isEnabled3}
          />)}
          { !isEnabled1 &&
          (<Text style = {[styles.text, {marginVertical: 10, backgroundColor: "white", padding: 10, borderRadius: 5,},]}>
            開關電燈</Text>)}
          { !isEnabled1 &&
            (<Switch
            trackColor={{ false: "#767577", true: "green" }}
            thumbColor={isEnabled4 ? "#fff" : "#fff"}
            ios_backgroundColor="#3e3e3e"
            onValueChange={toggleSwitch3}
            value={isEnabled4}
          />)}
          {!!error && <Text style={[styles.text, {margin: 10, color: 'red'}]}>Error Occurs!</Text>}
          {!!data && !error && 
            <Text style={[styles.text, {margin: 10, color: 'black'}]}>
              目前濕度：{data.moist}%   目前溫度：{data.temp}°C
            </Text>
          }
          { <Button title="Refresh Now" onPress={()=>mutate()}></Button> }
    </View>
  );
}

let styles = StyleSheet.create({
  container:{
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  text: {
    fontSize: 20,
    fontWeight: 500,
  },
  link: {
    fontSize: 20,
    fontWeight: 500,
    color: 'blue',
    marginVertical: 10,
  },
  footerText: {
    position: "absolute", // 絕對定位
    bottom: 10, // 距離底部的距離
    width: "100%", // 確保文字寬度與螢幕一致
    textAlign: "center", // 文字水平置中
    color: "lightgray", // 文字顏色為亮灰色
    fontSize: 15, // 字體大小為 15px
  },
})