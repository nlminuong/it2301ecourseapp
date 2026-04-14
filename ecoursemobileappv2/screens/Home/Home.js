import { useEffect, useState } from "react";
import { View, FlatList, ActivityIndicator, Image } from "react-native";
import { List } from "react-native-paper";
import Apis, { endpoints } from "../../configs/Apis";

const Home = () => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(false);

    const loadCourses = async () => {
        try {
            setLoading(true);
            let url = endpoints['courses'];
            let res = await Apis.get(url);
            setCourses(res.data.results);
        } catch (ex) {
            console.error(ex);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadCourses();
    }, []);

    return (
        <View>
            <FlatList
                data={courses}
                keyExtractor={(item) => item.id.toString()}
                renderItem={({ item }) => (
                    <List.Item
                        title={item.subject}
                        description={item.created_date}
                        left={() => (
                            <Image
                                style={{ width: 50, height: 50 }}
                                source={{ uri: item.image }}
                            />
                        )}
                    />
                )}
            />
            {loading && <ActivityIndicator />}
        </View>
    );
};

export default Home;