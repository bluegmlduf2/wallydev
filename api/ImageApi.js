import BaseApi from './BaseApi'

class ImageApi extends BaseApi {
  /**
   * The constructor for the ArtistApi.
   *
   * @param {Object} parameters The query parameters.
   */
  constructor(parameters = {}) {
    // BaseApi.js의 부모의 constructor를 실행, 부모의 endpoint는 reclist사용
    super('api_wallydev/image', parameters)
  }

  /**
   * 게시물 이미지 업로드
   *
   * @returns {Promise} The result in a promise.
   */
  uploadImage(param) {
    // uploadImage를 메서드명으로하면 중복호출이 일어나서 uploadImageSend로 정의
    return this.uploadImageSend(param)
  }
}

export default ImageApi
