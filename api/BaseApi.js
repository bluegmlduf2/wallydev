import Vue from 'vue';
class BaseApi {
  /**
   * The constructor of the BaseApi.
   *
   * @param {string} endpoint   엔드포인트 url, 자식 class에서 지정
   * @param {Object} parameters 서버로 전달할 파라미터, 자식 class에서 지정
   */
  constructor(endpoint, parameters = {}) {
    this.endpoint = endpoint
    this.parameters = parameters
  }

  /**
   * 전달할 파라미터의 중에서 복수의 값을 추가/수정한다.(추가/수정할 값을 키,값형태의 객체로 전달)
   *
   * @param {Object} parameters 추가/수정할 객체, 해당 키가 전달할 파라미터에 존재할 경우 수정, 없을경우 추가.
   *
   * @returns {BaseApi} The instance of the Api.
   */
  setParameters(parameters) {
    Object.keys(parameters).forEach((key) => {
      this.parameters[key] = parameters[key]
    })

    return this
  }

  /**
   * 전달할 파라미터의 중에서 하나의 값을 추가/수정한다.(추가/수정할 값을 키와 값으로 전달)
   *
   * @param {string} parameter 추가/수정할 키명
   * @param {*} value 추가/수정할 값
   *
   * @returns {BaseApi} The instance of the Api.
   */
  setParameter(parameter, value) {
    this.parameters[parameter] = value

    return this
  }

  /**
   * 전달할 파라미터의 중에서 복수의 값을 삭제한다.(삭제할 파라미터의 키값을 배열로 전달)
   *
   * @param {Array} parameters 삭제할 파라미터명의 키값이 들어간 배열.
   *
   * @returns {BaseApi} The instance of the Api.
   */
  removeParameters(parameters) {
    parameters.forEach((parameter) => {
      delete this.parameters[parameter]
    })

    return this
  }

  /**
   * 전달할 파라미터의 중에서 하나의 값을 삭제한다.(삭제할 파라미터의 키값을 문자열로 전달)
   *
   * @param {string} parameter 삭제할 파라미터명의 문자열.
   *
   * @returns {BaseApi} The instance of the Api.
   */
  removeParameter(parameter) {
    delete this.parameters[parameter]

    return this
  }

  /**
   *  AJAX-request를 이용해서 데이터를 가져온다
   *  (request method타입, 복수파라미터전송등 조금 더 세부적인 요청이 가능함)
   *
   * @param {string}      requestType The request type.
   * @param {string}      url         The URL for the request.
   * @param {Object|null} data        The data to be send with the request.
   *
   * @returns {Promise} The result in a promise.
   */
  submit(requestType, url, data = null) {
    return new Promise((resolve, reject) => {
      Vue.$http[requestType](url + this.getParameterString(), data)
        .then((response) => {
          resolve(response.data)
        })
        .catch(({ response }) => {
          if (response) {
            reject(response.data)
          } else {
            reject(response)
          }
        })
    })
  }

  /**
   * 파라미터없이 모든 데이터를 가져올때
   *
   * @returns {Promise} The result in a promise.
   */
  all() {
    return this.submit('get', `/${this.endpoint}`)
  }

  /**
   * 하나의 데이터를 가져올때
   *
   * @param {int} id The given identifier.
   *
   * @returns {Promise} The result in a promise.
   */
  find(id) {
    return this.submit('get', `/${this.endpoint}/${id}`)
  }

  /**
   * 데이터 등록
   *
   * @param {Object} item The given item.
   *
   * @returns {Promise} The result in a promise.
   */
  create(item) {
    return this.submit('post', `/${this.endpoint}`, item)
  }

  /**
   * 데이터 수정
   *
   * @param {int}    id   The given identifier.
   * @param {Object} item The given item.
   *
   * @returns {Promise} The result in a promise.
   */
  update(id, item) {
    // id가 존재하면 해당 id를 url에 넣고 없으면 id를 파라미터에 넣어서 보낸다
    const url = id ? `/${this.endpoint}/${id}` : `/${this.endpoint}`
    return this.submit('put', url, item)
  }

  /**
   * 이미지 업로드
   *
   * @param {Object} item The given item.
   *
   * @returns {Promise} The result in a promise.
   */
  uploadTempImage(item, isUserImgUpload = false) {
    // Post요청의 Content-Type 을 multipart/form-data(이미지 문자를 인코딩하지 않음)으로 설정하고 보낼수있음
    Vue.$http.defaults.headers.post['Content-Type'] = 'multipart/form-data'
    // userImgUrl가 참이면 하면 유저이미지 업로드, 존재하지않으면 게시물 업로드용
    const url = isUserImgUpload
      ? `/${this.endpoint}/userimage`
      : `/${this.endpoint}`
    return this.submit('post', url, item)
  }

  /**
   * 데이터 삭제
   *
   * @param {int} id The given identifier.
   *
   * @returns {Promise} The result in a promise.
   */
  destroy(id) {
    return this.submit('delete', `/${this.endpoint}/${id}`)
  }

  /**
   * 현재 설정된 파라미터를 쿼리파라미터 형식으로 만든다
   *
   * @returns {string} The parameter string.
   */
  getParameterString() {
    const keys = Object.keys(this.parameters)

    const parameterStrings = keys
      .filter((key) => !!this.parameters[key])
      .map((key) => `${key}=${this.parameters[key]}`)

    return parameterStrings.length === 0 ? '' : `?${parameterStrings.join('&')}`
  }
}

export default BaseApi
