<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <v-card class="mx-auto" max-width="500">
        <v-card dark flat>
          <v-btn absolute bottom color="maincolor" right fab>
            <v-icon>mdi-plus</v-icon>
          </v-btn>
          <v-card-title class="pa-2 maincolor">
            <h3 class="text-h5 pl-10 font-weight-light text-center grow">Timeline</h3>
            <v-avatar>
              <v-img
                src="https://avataaars.io/?avatarStyle=Circle&topType=ShortHairShortRound&accessoriesType=Blank&hairColor=Black&facialHairType=Blank&clotheType=BlazerSweater&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
              ></v-img>
            </v-avatar>
          </v-card-title>
          <v-img
            src="https://cdn.vuetifyjs.com/images/cards/forest.jpg"
            gradient="to top, rgba(0,0,0,.44), rgba(0,0,0,.44)"
          >
            <v-container class="fill-height">
              <v-row justify="end">
                <div class="text-h5 font-weight-light">Keep going..</div>
              </v-row>
            </v-container>
          </v-img>
        </v-card>
        <v-card-text class="py-0">
          <v-timeline align-top dense>
            <v-timeline-item color="teal lighten-3" small>
              <v-row class="pt-1">
                <v-col cols="4">
                  <strong>2018.04.01</strong>
                </v-col>
                <v-col>
                  <span>개발자 경력의 시작</span>
                </v-col>
              </v-row>
            </v-timeline-item>

            <v-timeline-item color="teal lighten-3" small>
              <v-row class="pt-1">
                <v-col cols="4">
                  <strong>2020.01.01</strong>
                </v-col>
                <v-col>
                  <span>일본생활 시작</span>
                </v-col>
              </v-row>
            </v-timeline-item>

            <v-timeline-item color="teal lighten-3" small>
              <v-row class="pt-1">
                <v-col cols="4">
                  <strong>2022.09.01</strong>
                </v-col>
                <v-col>
                  <span>개인 프로젝트 플랜몬 오픈</span>
                </v-col>
              </v-row>
            </v-timeline-item>

            <v-timeline-item color="teal lighten-3" small>
              <v-row class="pt-1">
                <v-col cols="4">
                  <strong>{{ currentDate }}</strong>
                </v-col>
                <v-col>
                  <span
                    >개발자로 성장중 <v-icon small>mdi-laptop</v-icon>
                  </span>
                </v-col>
              </v-row>
            </v-timeline-item>
          </v-timeline>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text nuxt to="/inspire"> GitHub </v-btn>
          <v-btn text nuxt to="/inspire"> Planmon </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'IndexPage',
  computed: {
    currentDate() {
      const today = new Date()
      const yyyy = today.getFullYear()
      const mm = String(today.getMonth() + 1).padStart(2, '0')
      const dd = String(today.getDate()).padStart(2, '0')

      return `${yyyy}.${mm}.${dd}`
    },
  },
}
</script>
