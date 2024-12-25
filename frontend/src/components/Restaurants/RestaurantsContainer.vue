<template>
  <div class="restaurants-container">
    <div v-if="!selectedRestaurant" class="row">
      <b class="sticky-top" style="background:white;">Restaurants nearby your address</b>
      <restaurant-preview-card
        v-for="(restaurant, index) in restaurants"
        :key="restaurant.uuid"
        :restaurant="restaurant"
        :idx="index"
        @restaurant-clicked="selectRestaurant"
        class="col-md-4 col-lg-3"
      ></restaurant-preview-card>
    </div>
    <restaurant-full-view
      ref="restaurantFullView"
      v-show="selectedRestaurant"
      :restaurant="selectedRestaurant"
      @go-back="deselectRestaurant"
      @add-to-cart="addToCart"
      @register-action="registerAction"
    ></restaurant-full-view>
  </div>
</template>

  <script>
  import RestaurantPreviewCard from "./RestaurantPreviewCard.vue";
  import RestaurantFullView from "./RestaurantFullView.vue"
  import "../styles/restaurants.css"
  import axios from "axios";

  export default {
    components: {
      RestaurantPreviewCard,
      RestaurantFullView
    },
    data() {
      return {
        selectedRestaurant: null,
        baseApiUrl: import.meta.env.VITE_APP_API_URL + "/api",
        restaurants: []
      };
    },
    methods: {
      registerAction(msg) {
        this.$emit("register-action", msg)
      },
      addToCart(item){
        this.$emit("add-to-cart", item)
      },
      selectRestaurant(uuid) {
        let flag_register_new_action = true;
        if (this.selectedRestaurant) {
          if (this.selectedRestaurant.uuid === uuid) {
            flag_register_new_action = false;
          }
        }

        this.selectedRestaurant = this.restaurants.find(
          (restaurant) => restaurant.uuid === uuid
        );
        if (this.$refs.restaurantFullView) {
          this.$refs.restaurantFullView.getFoods(this.selectedRestaurant);
        }
        if (flag_register_new_action){
          this.registerAction("opened the restaurant page " + this.selectedRestaurant.name + " with restaurant_uuid=" + this.selectedRestaurant.uuid)
        }
      },
      deselectRestaurant() {
        this.registerAction("closed the restaurant page " + this.selectedRestaurant.name)
        this.selectedRestaurant = null;
      },
      async getRestaurants() {
        try {
          const response = await axios.get(`${this.baseApiUrl}/restaurants`);
          this.restaurants = response.data.map(restaurant => ({
            name: restaurant.name,
            description: restaurant.description,
            uuid: restaurant.id,
            image: restaurant.image ? `${import.meta.env.VITE_APP_API_URL}${restaurant.image}` : null
          }));
        } catch (error) {
          console.error('Error fetching restaurants:', error);
        }
      },
    },
    mounted() {
      this.getRestaurants();
    },
  };
  </script>