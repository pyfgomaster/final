import { defaultFetcher } from "@/api/fetcher";
import { Stack } from "expo-router";
import React from "react";
import { View, Text, Image } from "react-native";
import { SWRConfig } from "swr";

export default function RootLayout() {
  return(
    <SWRConfig value={{
      shouldRetryOnError: false,
      fetcher: defaultFetcher
    }}>
      <Stack>
        <Stack.Screen name="index" options={{headerTitle:()=>(
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <Image source={require('@/小鐘同學.png')} 
                  style={{ width: 50, height: 50, marginRight: 5, borderRadius: 20}}/>
            <Text style={{fontSize: 20}}> 小鐘同學</Text>
          </View>
        )}}/>
      </Stack>
    </SWRConfig>
  );
}
