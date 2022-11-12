import BaseApi from './BaseApi'

class PostApi extends BaseApi {
  /**
   * The constructor for the ArtistApi.
   *
   * @param {Object} parameters The query parameters.
   */
  constructor(parameters = {}) {
    // BaseApi.js의 부모의 constructor를 실행, 부모의 endpoint는 reclist사용
    super('api_wallydev/post', parameters)
  }

  /**
   * 게시물 가져오기
   *
   * @param {String} postId 게시물 번호
   *
   * @returns {Promise} The result in a promise.
   */
  getPost(postId) {
    return this.find(postId)
  }

  /**
   * 게시물 등록
   *
   * @returns {Promise} The result in a promise.
   */
  createPost(param) {
    return this.create(param)
  }

  /**
   * 게시물 수정
   *
   * @returns {Promise} The result in a promise.
   */
  updatePost(param) {
    return this.update(param)
  }

  /**
   * 게시물 삭제
   *
   * @returns {Promise} The result in a promise.
   */
  deletePost(param) {
    return this.delete(param)
  }
}

export default PostApi
