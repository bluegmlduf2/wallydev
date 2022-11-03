import BaseApi from './BaseApi'

class CommentApi extends BaseApi {
  /**
   * The constructor for the ArtistApi.
   *
   * @param {Object} parameters The query parameters.
   */
  constructor(parameters = {}) {
    // BaseApi.js의 부모의 constructor를 실행, 부모의 endpoint는 reclist사용
    super('comment', parameters)
  }

  /**
   * 댓글 등록
   *
   * @returns {Promise} The result in a promise.
   */
  createComment(param) {
    return this.create(param)
  }

  /**
   * 댓글 수정
   *
   * @returns {Promise} The result in a promise.
   */
  updateComment(param) {
    return this.update(param)
  }

  /**
   * 댓글 삭제
   *
   * @returns {Promise} The result in a promise.
   */
  deleteComment(param) {
    return this.delete(param)
  }
}

export default CommentApi
